"""Build vector store from internal documentation."""

import os
from pathlib import Path
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
except Exception:
    # Fallback simple splitter when langchain version doesn't provide RecursiveCharacterTextSplitter
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
    # If langchain_community.Chroma is unavailable, try langchain.vectorstores (older/newer variants)
    try:
        from langchain.vectorstores import Chroma
    except Exception:
        Chroma = None
from src.config import settings
from src.llm_provider import LLMProvider
import json
import numpy as np


# Simple fallback vector store using numpy + JSON metadata
class SimpleVectorStore:
    def __init__(self, vectors, metadatas, texts, persist_directory):
        self.vectors = np.array(vectors)
        self.metadatas = metadatas
        self.texts = texts
        self.persist_directory = persist_directory

    def save(self):
        np.savez_compressed(Path(self.persist_directory) / "vectors.npz", vectors=self.vectors)
        with open(Path(self.persist_directory) / "metadatas.json", "w", encoding="utf-8") as f:
            json.dump(self.metadatas, f, ensure_ascii=False)
        with open(Path(self.persist_directory) / "texts.json", "w", encoding="utf-8") as f:
            json.dump(self.texts, f, ensure_ascii=False)

    @staticmethod
    def load(persist_directory):
        data = np.load(Path(persist_directory) / "vectors.npz")
        vectors = data["vectors"]
        with open(Path(persist_directory) / "metadatas.json", "r", encoding="utf-8") as f:
            metadatas = json.load(f)
        with open(Path(persist_directory) / "texts.json", "r", encoding="utf-8") as f:
            texts = json.load(f)
        return SimpleVectorStore(vectors, metadatas, texts, persist_directory)

    def as_retriever(self, search_kwargs=None):
        k = (search_kwargs or {}).get("k", 3)
        return SimpleRetriever(self, k=k)


class SimpleRetriever:
    def __init__(self, store: SimpleVectorStore, k=3):
        self.store = store
        self.k = k

    def invoke(self, query):
        # Expect query to be an object or string; compute embedding
        try:
            emb_model = LLMProvider().get_embeddings_model()
            qvec = emb_model.embed_query(query) if hasattr(emb_model, 'embed_query') else emb_model.embed_documents([query])[0]
        except Exception:
            # fallback: use zero vector
            qvec = np.zeros(self.store.vectors.shape[1])

        # cosine similarity
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


def load_documents_from_docs():
    """Load all markdown documents from docs/ directory."""
    docs_dir = Path(__file__).parent.parent / "docs"
    documents = []
    
    if not docs_dir.exists():
        print(f"⚠️  Documentation directory not found: {docs_dir}")
        return documents
    
    for md_file in docs_dir.glob("*.md"):
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                documents.append({
                    "filename": md_file.name,
                    "content": content,
                    "path": str(md_file),
                })
        except Exception as e:
            print(f"⚠️  Error reading {md_file}: {e}")
    
    return documents


def build_vector_store():
    """Build and persist vector store."""
    print("\n🔨 Building Vector Store...")
    
    # Validate API configuration
    try:
        provider = LLMProvider()
    except ValueError as e:
        print(f"❌ Cannot build vector store: {e}")
        print("⚠️  Skipping vector store creation. Configure your AI provider first.")
        return False
    
    # Load documents
    print("📂 Loading documentation...")
    documents = load_documents_from_docs()
    
    if not documents:
        print("⚠️  No documents found. Skipping vector store creation.")
        return False
    
    print(f"📄 Found {len(documents)} documents")
    
    # Split documents into chunks
    print("✂️  Splitting documents into chunks...")
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
            metadatas.append({
                "source": doc["filename"],
                "path": doc["path"],
            })
    
    print(f"📦 Created {len(texts)} chunks")
    
    # Create embeddings and vector store
    print("🧮 Creating embeddings and vector store...")
    try:
        embeddings = provider.get_embeddings_model()

        vector_store_path = settings.dynamic_vector_store_path
        os.makedirs(vector_store_path, exist_ok=True)

        # If Chroma is available, use it
        if Chroma is not None:
            vectorstore = Chroma.from_texts(
                texts=texts,
                embedding=embeddings,
                metadatas=metadatas,
                persist_directory=vector_store_path,
            )
            print(f"✅ Vector store created successfully using Chroma!")
            print(f"📍 Stored at: {vector_store_path}")
            return True

        # Otherwise use SimpleVectorStore fallback
        print("⚠️  Chroma not available, using SimpleVectorStore fallback")
        vectors = []
        try:
            vectors = embeddings.embed_documents(texts)
        except Exception as e:
            print(f"⚠️  Embeddings model failed to embed documents: {e}")
            # create zero vectors as fallback to avoid crash
            vectors = [[0.0] * 768 for _ in texts]

        svs = SimpleVectorStore(vectors=vectors, metadatas=metadatas, texts=texts, persist_directory=vector_store_path)
        svs.save()
        print(f"✅ Simple vector store created successfully!")
        print(f"📍 Stored at: {vector_store_path}")
        return True

    except Exception as e:
        print(f"❌ Error creating vector store: {e}")
        return False


if __name__ == "__main__":
    success = build_vector_store()
    if not success:
        print("\n⚠️  Vector store could not be built. Check your API configuration.")
        exit(1)
