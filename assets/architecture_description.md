# 🏗️ Architecture de l'Application

## Vue d'ensemble globale

```
┌──────────────────────────────────────────────────────────────────┐
│                     🌐 Frontend Streamlit                         │
│  ┌────────────┬──────────┬──────────┬──────────┬──────────────┐  │
│  │  Accueil   │ Chat RAG │ Compta   │Fourniss. │ Trésorerie   │  │
│  │  Budget    │ Qualité  │ Commen   │ - + 3    │              │  │
│  └────────────┴──────────┴──────────┴──────────┴──────────────┘  │
└────────────────────────┬─────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼─────┐   ┌────▼──────┐  ┌────▼──────┐
    │   Chat   │   │ Analytics │  │ Raw Data  │
    │   RAG    │   │ Modules   │  │ Loader    │
    └────┬─────┘   └────┬──────┘  └────┬──────┘
         │               │              │
         └───────────────┼──────────────┘
                         │
         ┌───────────────▼──────────────┐
         │   LLM Provider (Gemini/Groq)│
         │   Embeddings API             │
         └──────────────────────────────┘
         
         ┌──────────────────────────────┐
         │   ChromaDB Vector Store      │
         │   (Docs + Procedures)        │
         └──────────────────────────────┘
```

## 1. Architecture en couches

### Couche Présentation (Streamlit)
- **app.py** : Point d'entrée unique
- Pages multiples avec routage
- Session state pour persistence
- Caching pour performance

**Pages**
1. Home : Vue d'ensemble + configuration
2. Chat IA : Interface Q&A avec RAG
3. Comptabilité : Balance et contrôles
4. Fournisseurs : Suivi factures
5. Trésorerie : Cash flow et prévisions
6. Budget : Contrôle vs réel
7. Qualité : Scores et anomalies
8. Commentaire : Génération IA

### Couche Métier (Business Logic)
- **accounting_analyzer.py** : Analyse comptabilité générale
- **finance_analyzer.py** : Budget et OPEX/CAPEX
- **supplier_accounting.py** : Fournisseurs et délais paiement
- **treasury_analyzer.py** : Trésorerie et liquidité
- **quality_checker.py** : Validation qualité données
- **management_commentary.py** : Génération textes

### Couche IA & RAG
- **rag_pipeline.py** : Pipeline complet RAG
- **llm_provider.py** : Abstraction LLM (Gemini/Groq)
- **prompt_templates.py** : Prompts centralisés

### Couche Données
- **data_loader.py** : Chargement CSV
- **config.py** : Settings et configuration
- **security.py** : Gestion secrets

## 2. Flux de données

### A. Flux Chargement Données
```
CSV Files (data/)
    ↓
DataLoader.load_all_data()
    ↓
Pandas DataFrame (in-memory)
    ↓
@st.cache_resource (Streamlit cache)
    ↓
Analyzers consume DataFrames
```

### B. Flux Chat RAG
```
User Question
    ↓
RAGPipeline.query(question)
    ↓
[1] ChromaDB similarity search
    ↓ (retrieves similar docs)
[2] LLMProvider.get_chat_model()
    ↓
[3] Gemini API call with context
    ↓
    ├─ Answer ✓
    ├─ Sources []
    ↓
Display in Streamlit
```

### C. Flux Analyse
```
Raw Data (CSV)
    ↓
initialize_analyzers()
    ↓
┌─────────────────────────────────────┐
│ Accounting (balance, anomalies)     │
│ Finance (budget vs real)            │
│ Supplier (invoices, delays)         │
│ Treasury (cash flow, forecast)      │
│ Quality (scores, recommendations)   │
└─────────────────────────────────────┘
    ↓
render_[page]()
    ↓
Plotly Charts + Metrics + Tables
```

## 3. Modèle de données Star Schema

### Fact Tables
- **fact_ecritures_comptables** : Écritures comptables brutes
- **fact_factures_fournisseurs** : Factures avec détails
- **fact_budget** : Budget par centre et mois
- **fact_tresorerie** : Flux de trésorerie quotidiens
- **fact_rapprochement_bancaire** : Mouvements rapprochés

### Dimension Tables
- **dim_compte_comptable** : Plan comptable
- **dim_centre_cout** : Centres d'analyse
- **dim_projet** : Projets et revenus
- **dim_fournisseur** : Référentiel fournisseurs
- **dim_date** : Calendar dimension

## 4. Cycle de vie des données

### Phase 1 : Initialisation
```
generate_demo_data.py
    ↓
Crée 10 fichiers CSV
    ↓
data/ directory
    ↓
Seed = 42 (reproducibilité)
```

### Phase 2 : Chargement
```
App startup
    ↓
@st.cache_resource load_data()
    ↓
DataLoader.load_all_data()
    ↓
Chargé une seule fois par session
```

### Phase 3 : Analyse
```
initialize_analyzers()
    ↓
Chaque analyzer = nouvelle instance
    ↓
Chaque page = calculs à la demande
    ↓
Plots et métriques générés
```

### Phase 4 : Cache
```
Streamlit @st.cache_resource
    ↓
    ├─ load_data()
    ├─ initialize_analyzers()
    └─ LLMProvider config
    ↓
Reutilisé pour toute la session
```

## 5. Module RAG Pipeline

### Components
```
RAGPipeline
    ├─ Document Loader
    │   ├─ Lit tous les .md dans docs/
    │   └─ Chunking avec recursive splitter
    │
    ├─ Embeddings
    │   ├─ Gemini Embedding Model
    │   └─ Crée vecteurs 768-dim
    │
    ├─ Vector Store
    │   ├─ ChromaDB (persistent)
    │   └─ Stocke embeddings + metadata
    │
    └─ Retrieval Chain
        ├─ Similarity search (k=3)
        ├─ LLMProvider chat model
        └─ Returns (answer, sources)
```

### Flux Query
```
query(question, k=3)
    ↓
[1] Embed question
    ↓ (768-dim vector)
[2] Search ChromaDB
    ↓ (top-k similar chunks)
[3] Build context prompt
    ↓ (chunks + question)
[4] Call LLM with context
    ↓ (Gemini API)
[5] Format response
    ↓ (answer + source metadata)
Return → Streamlit
```

## 6. LLM Provider Strategy

### Abstraction Design
```
LLMProvider (classe statique)
    ├─ get_chat_model()
    │   ├─ Si provider = "gemini" → Gemini API
    │   └─ Si provider = "groq" → Groq API
    │
    ├─ get_embeddings_model()
    │   └─ Toujours Gemini (fiable + rapide)
    │
    ├─ is_api_available()
    │   └─ Teste connectivité API
    │
    └─ get_provider_info()
        └─ Status + config (masqué keys)
```

### Fallback Strategy
```
Primary (Gemini)
    ↓ (si ko)
Fallback (Groq)
    ↓ (si ko)
Offline Mode (rule-based fallback)
```

## 7. Configuration & Secrets

### Hiérarchie Config
```
.env (user's secrets)
    ↓
settings = Settings() (pydantic)
    ↓
Validated environment variables
    ↓
Used by:
    ├─ LLMProvider
    ├─ RAGPipeline
    └─ Streamlit app
```

### Environment Variables
- `AI_PROVIDER` : Choix provider
- `GEMINI_API_KEY` : Gemini auth
- `GROQ_API_KEY` : Groq auth
- `CHUNK_SIZE` : RAG parameter
- `CHUNK_OVERLAP` : RAG parameter
- `TEMPERATURE` : LLM param
- `MAX_TOKENS` : LLM param

## 8. Analyzers Design Pattern

### Template
```
class AnalyzerName:
    def __init__(self, data_df1, data_df2):
        self.data = data
        self._cache = {}
    
    def get_summary(self):
        """Retour agrégé."""
        pass
    
    def get_detail(self):
        """Retour détaillé."""
        pass
    
    def detect_issues(self):
        """Détection anomalies."""
        pass
```

### Chaque analyzer
- Reçoit données nécessaires au construction
- Méthodes sans état (pure functions)
- Cache interne pour perf
- Retourne dict ou DataFrame

## 9. Error Handling

### Stratégies
```
Data Missing
    ↓
st.error("Données non chargées")
    └─ Affiche message utilisateur

LLM Unavailable
    ↓
Use fallback method
    └─ Texte template ou règles

API Error
    ↓
Retry + log + notify user
    └─ Graceful degradation

Validation Error
    ↓
Suggestions autocorrection
    └─ Dans qualité module
```

## 10. Performance Optimization

### Caching Strategy
```
@st.cache_resource
def load_data():
    # Chargé une fois
    # Réutilisé pour toute la session
    # Même si user change pages

Per-analyzer cache:
    # Chaque analyzer a dict interne
    # Résultats calculés une fois
```

### Lazy Loading
- Analyzers = créés à la demande
- Chartes = générées seulement si page affichée
- RAG = construit seulement si chat utilisé

### Data Size Management
- CSV modérés (< 1M rows)
- Pandas DataFrames in-memory
- Aggégation avant visualisation
- Plotly (optimisé client-side)

## 11. Deployment Architecture

### Local Development
```
poetry/venv
    ↓
python app.py
    ↓
Streamlit dev server :8501
```

### Streamlit Cloud
```
GitHub repo
    ↓
Streamlit Cloud detects app.py
    ↓
Deploys container
    ↓
Public URL
```

### Azure Container Apps / Kubernetes
```
Dockerfile (app + dependencies)
    ↓
Docker image build
    ↓
Registry push
    ↓
ACA/K8s deployment
    ↓
Scaling + monitoring
```

## 12. Monitoring & Logging

### Points de monitoring
- API disponibilité (LLM)
- Temps d'exécution queries
- Erreurs données (qualité)
- User interactions (audit)

### Logging Strategy
```
streamlit_logger = logging.getLogger(__name__)
    ↓
Log configuration:
    ├─ DEBUG : Code flow details
    ├─ INFO : Major operations
    ├─ WARNING : Potential issues
    └─ ERROR : Failures
    ↓
Logs → stdout + file (optional)
```

## 13. Security Architecture

### Authentication (Future)
```
User Login
    ↓
Entra ID / OAuth2
    ↓
Session token
    ↓
Access control per page
```

### Data Protection
- Secrets in .env
- API keys masked
- Audit logging possible
- User data isolation

### API Security
```
Rate limiting (future)
    ├─ Per user
    └─ Per LLM endpoint

Input validation
    ├─ Question length
    ├─ Query parameters
    └─ SQL injection prevention
```

## 14. Testing Strategy

### Unit Tests
- Analyzer methods
- Data validation
- Calculation correctness

### Integration Tests
- Data loader + analyzers
- LLM + RAG flow
- Error handling

### End-to-End
- Full app flow
- Multiple pages
- Cache + session state

```bash
pytest tests/ -v --cov
```

---

**Contenu régulièrement mis à jour comme la base de code évolue.**
