"""RAG pipeline for document retrieval and QA."""

import os
from pathlib import Path
from typing import Optional, Tuple, List
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
except Exception:
    class RecursiveCharacterTextSplitter:
        def __init__(self, chunk_size=1000, chunk_overlap=200, separators=None):
            self.chunk_size = chunk_size
            self.chunk_overlap = chunk_overlap

        def split_text(self, text: str):
            chunks = []
            n = len(text)
            step = max(1, self.chunk_size - self.chunk_overlap)
            i = 0
            while i < n:
                chunks.append(text[i : i + self.chunk_size])
                i += step
            return chunks

try:
    from langchain_community.vectorstores import Chroma
except Exception:
    try:
        from langchain.vectorstores import Chroma
    except Exception:
        Chroma = None
try:
    from langchain.chains import RetrievalQA
except Exception:
    RetrievalQA = None
from src.config import settings
from src.llm_provider import LLMProvider
from src.prompt_templates import RAG_SYSTEM_PROMPT, GENERAL_FINANCE_QUESTION_PROMPT
import json
import numpy as np
from pathlib import Path


# SimpleVectorStore fallback loader for previously persisted simple stores
class SimpleVectorStore:
    def __init__(self, vectors, metadatas, texts):
        self.vectors = np.array(vectors)
        self.metadatas = metadatas
        self.texts = texts

    @staticmethod
    def load(persist_directory):
        dirp = Path(persist_directory)
        data = np.load(dirp / "vectors.npz")
        vectors = data["vectors"]
        with open(dirp / "metadatas.json", "r", encoding="utf-8") as f:
            metadatas = json.load(f)
        with open(dirp / "texts.json", "r", encoding="utf-8") as f:
            texts = json.load(f)
        return SimpleVectorStore(vectors=vectors, metadatas=metadatas, texts=texts)

    def as_retriever(self, search_kwargs=None):
        k = (search_kwargs or {}).get("k", 3)
        return SimpleRetriever(self, k=k)


class SimpleRetriever:
    def __init__(self, store: SimpleVectorStore, k=3):
        self.store = store
        self.k = k

    def invoke(self, query):
        try:
            emb_model = LLMProvider().get_embeddings_model()
            qvec = emb_model.embed_query(query) if hasattr(emb_model, 'embed_query') else emb_model.embed_documents([query])[0]
        except Exception:
            qvec = np.zeros(self.store.vectors.shape[1])

        vecs = self.store.vectors
        norms = np.linalg.norm(vecs, axis=1) * (np.linalg.norm(qvec) + 1e-12)
        sims = (vecs @ qvec) / norms
        idxs = np.argsort(-sims)[: self.k]

        class Doc:
            def __init__(self, page_content, metadata):
                self.page_content = page_content
                self.metadata = metadata

        results = [Doc(self.store.texts[i], self.store.metadatas[i]) for i in idxs]
        return results


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline for finance documents."""

    def __init__(self):
        """Initialize RAG pipeline."""
        self.documents_dir = Path(__file__).parent.parent / "docs"
        self.vector_store_path = settings.vector_store_path
        self.vectorstore = None
        self.llm = None
        self.embeddings = None
        self._initialize()

    def _initialize(self):
        """Initialize LLM and vector store."""
        try:
            provider = LLMProvider()
            self.llm = provider.get_chat_model()
            self.embeddings = provider.get_embeddings_model()
            self._load_or_build_vector_store()
        except Exception as e:
            print(f"⚠️  RAG Pipeline initialization error: {e}")

    def _load_or_build_vector_store(self):
        """Load existing vector store or build a new one."""
        if os.path.exists(self.vector_store_path):
            # If Chroma is available, try to load it
            if Chroma is not None:
                try:
                    self.vectorstore = Chroma(
                        persist_directory=self.vector_store_path,
                        embedding_function=self.embeddings,
                    )
                    print("✅ Vector store loaded (Chroma)")
                    return
                except Exception as e:
                    print(f"⚠️  Could not load Chroma vector store: {e}")

            # Try SimpleVectorStore persisted format
            try:
                simple = SimpleVectorStore.load(self.vector_store_path)
                self.vectorstore = simple
                print("✅ Simple vector store loaded")
                return
            except Exception as e:
                print(f"⚠️  Could not load simple vector store: {e}")

            # Fallback to building
            self._build_vector_store()
        else:
            self._build_vector_store()

    def _build_vector_store(self):
        """Build vector store from documents."""
        print("🔨 Building vector store from documents...")

        documents = self._load_documents()
        if not documents:
            print("⚠️  No documents found")
            return

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            separators=["\n\n", "\n", " ", ""],
        )

        texts = []
        metadatas = []

        for doc in documents:
            chunks = text_splitter.split_text(doc["content"])
            for chunk in chunks:
                texts.append(chunk)
                metadatas.append({"source": doc["filename"]})

        if texts:
            os.makedirs(self.vector_store_path, exist_ok=True)
            self.vectorstore = Chroma.from_texts(
                texts=texts,
                embedding=self.embeddings,
                metadatas=metadatas,
                persist_directory=self.vector_store_path,
            )
            print(f"✅ Vector store built with {len(texts)} chunks")

    def _load_documents(self) -> List[dict]:
        """Load all markdown documents."""
        documents = []

        if not self.documents_dir.exists():
            return documents

        for md_file in self.documents_dir.glob("*.md"):
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    documents.append({
                        "filename": md_file.name,
                        "content": f.read(),
                    })
            except Exception as e:
                print(f"⚠️  Error loading {md_file}: {e}")

        return documents

    def query(self, question: str, k: int = 3) -> Tuple[str, List[str]]:
        """Query the RAG pipeline."""
        if not self.vectorstore or not self.llm:
            return self._handle_no_llm(question), []

        try:
            retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
            docs = retriever.invoke(question)

            if not docs:
                return "Je n'ai pas trouvé d'information pertinente dans la base de connaissances.", []

            context = "\n".join([doc.page_content for doc in docs])
            sources = [doc.metadata.get("source", "Unknown") for doc in docs]

            prompt = GENERAL_FINANCE_QUESTION_PROMPT.format(
                context=context,
                question=question,
            )

            try:
                response = self.llm.invoke(prompt)
                answer = response.content if hasattr(response, 'content') else str(response)
            except Exception as llm_error:
                excerpt = "\n\n".join(doc.page_content[:350].strip() for doc in docs[:2])
                answer = (
                    "⚠️ Le modèle local n'a pas pu générer une réponse complète. "
                    f"Détail technique: {llm_error}\n\n"
                    "Extraits pertinents retrouvés dans la base documentaire:\n"
                    f"{excerpt}"
                )

            return answer, list(set(sources))

        except Exception as e:
            return f"Erreur lors du traitement: {e}", []

    def _handle_no_llm(self, question: str) -> str:
        """Handle case where LLM is not available."""
        return (
            "⚠️  Le modèle local n'est pas disponible pour générer une réponse. "
            "Vérifiez qu'Ollama est en cours d'exécution et que le modèle configuré est accessible. "
            f"\n\nVotre question: {question}"
        )

    def search_documents(self, query: str, k: int = 5) -> List[Tuple[str, str]]:
        """Search documents without generating answer."""
        if not self.vectorstore:
            return []

        try:
            retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
            docs = retriever.invoke(query)

            results = [
                (doc.page_content[:500], doc.metadata.get("source", "Unknown"))
                for doc in docs
            ]
            return results
        except Exception as e:
            print(f"⚠️  Search error: {e}")
            return []

    def get_available_topics(self) -> List[str]:
        """Get list of available documentation topics."""
        topics = []

        if self.documents_dir.exists():
            for md_file in self.documents_dir.glob("*.md"):
                topics.append(md_file.stem.replace("_", " ").title())

        return topics

    def is_ready(self) -> bool:
        """Check if RAG pipeline is ready."""
        return self.vectorstore is not None and self.llm is not None
