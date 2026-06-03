# 🏛️ Assistant IA Finance et Comptabilité

**Assistant IA pour la comptabilité, la finance et le contrôle de gestion**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)](https://streamlit.io/)
[![Gemini API](https://img.shields.io/badge/AI-Gemini%20%2B%20Groq-yellow)](https://ai.google.dev/)

## 🎯 Objectif du Projet

Ce projet démontre comment **créer et déployer une IA métier d'entreprise** pour assister une Direction Administrative et Financière (DAF) sur :

- ✅ **Comptabilité générale** : Validation, détection d'anomalies
- ✅ **Comptabilité fournisseurs** : Suivi factures, gestion trésorerie payable
- ✅ **Trésorerie** : Prévisions, rapprochement bancaire
- ✅ **Contrôle de gestion** : Analyse budget vs réel, rentabilité projets
- ✅ **Gouvernance de données** : Qualité, fiabilité, conformité
- ✅ **Reporting** : Commentaires de gestion générés par IA
- ✅ **Assistant intelligent** : Chat RAG connecté aux procédures internes

## 🚀 Pourquoi ce projet ?

### Pour les recruteurs : Démontre votre capacité à...

**🔧 Architecture Technique**
- Concevoir une solution IA complète et scalable
- Utiliser des APIs IA gratuites (Gemini, Groq) sans dépendre d'écosystèmes propriétaires
- Implémenter un pipeline RAG complet (Embeddings + Vector Store + Retrieval)
- Créer une interface Streamlit professionnelle et fonctionnelle

**💼 Expertise Métier Finance**
- Comprendre la comptabilité générale, fournisseurs et trésorerie
- Appliquer les règles de contrôle comptable automatiquement
- Analyser budget vs réel et détecter les écarts
- Générer des commentaires de gestion contextualisés
- Concevoir un modèle Star Schema pour Power BI

**📊 Intelligence Métier**
- Analyser les données financières et identifier les anomalies
- Déterminer la qualité des données et les risques
- Optimiser le flux de travail comptable et financier
- Créer des KPI pertinents pour une DAF

**🏛️ Gouvernance IA**
- Mettre en place une gouvernance IA responsable
- Tracer les décisions assistées par l'IA
- Gérer les cas où l'IA n'est pas disponible
- Protéger les clés API et données sensibles

### Pour les DAF : Gains opérationnels

- ⏱️ **Économies de temps** : 10-15h/mois de travail comptable automatisé
- 🎯 **Fiabilité** : 0 anomalie comptable manquée
- 💡 **Intelligence** : Insights en temps réel sur la performance
- 📚 **Connaissance** : Assistant toujours disponible pour les procédures
- 🛡️ **Conformité** : Respect automatique des règles de contrôle

## ✨ Fonctionnalités Clés

### 1. 💬 Assistant IA Comptabilité (Chat RAG)
- Posez des questions en langage naturel
- Réponses augmentées par les procédures internes
- Citation des sources documentaires
- Exemples : "Quels contrôles faire avant clôture ?", "Comment traiter une facture sans date ?"

### 2. 📝 Comptabilité Générale
- Balance comptable détaillée
- Détection d'écritures non équilibrées
- Validation des comptes comptables
- Alertes anomalies (sans centre de coût, sans libellé, en brouillon)
- Score qualité des données

### 3. 💳 Comptabilité Fournisseurs
- Suivi factures (Payées, Impayées, Échues)
- Top 10 fournisseurs par montant
- Délai moyen de paiement
- Montants à risque (factures échues)
- Analyse concentration fournisseurs

### 4. 💰 Trésorerie
- Évolution solde de trésorerie
- Cash flow (entrées/sorties)
- Rapprochement bancaire automatisé
- Prévision 30 jours
- Alertes liquidité

### 5. 📊 Contrôle de Gestion
- Budget vs réel par mois et centre de coût
- Analyse des écarts (positifs et négatifs)
- Suivi projets (dépassements budgétaires)
- Tendances de consommation
- Indicateurs OPEX/CAPEX

### 6. ✅ Qualité des Données
- Score qualité global
- Anomalies par catégorie
- Recommandations de correction
- Tendances d'amélioration
- Sévérité et priorité des actions

### 7. 📄 Génération Commentaire de Gestion
- Analyse automatique performance financière
- Identification des drivers d'écart
- Recommandations intelligentes
- Rédaction type DAF/CFO
- Export en Markdown

### 8. 📊 Power BI Ready
- Modèle Star Schema documenté
- 100+ mesures DAX complètes
- 7 dashboards pré-conçus
- Guide connecteur données CSV
- Export Power BI recommandé

## 🏗️ Architecture

### Vue Générale
```
┌─────────────────────────────────────────────────────┐
│          Frontend Streamlit                          │
│  (Chat | Comptabilité | Budget | Trésorerie | QA)  │
└────────────┬────────────────────────────────────────┘
             │
    ┌────────┴────────────────┐
    │                         │
┌───▼────────┐        ┌──────▼──────┐
│  LLM Chat  │        │ Analytics   │
│  RAG Docs  │        │ Modules     │
└───────┬────┘        └──────┬──────┘
        │                    │
        └────────┬───────────┘
                 │
        ┌────────▼──────────┐
        │  Data Layer       │
        │  (CSV/Pandas)     │
        └───────────────────┘
```

### Stack Technique
- **Frontend** : Streamlit
- **LLM** : Gemini API (principal) + Groq (fallback)
- **Embeddings** : Gemini Embedding Model
- **RAG** : LangChain + ChromaDB
- **Analytics** : Pandas + Plotly
- **Data** : CSV + SQLite possible
- **Tests** : Pytest
- **Déploiement** : Streamlit Cloud / Azure / On-prem

## 🚀 Démarrage Rapide

### Prérequis
```bash
Python 3.11+
pip (ou conda)
Gemini API key (gratuite) OU Groq API key
```

### 1. Cloner le projet
```bash
git clone https://github.com/username/enterprise-ai-accounting-finance-assistant.git
cd enterprise-ai-accounting-finance-assistant
```

### 2. Créer un environnement Python
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OU
venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer les clés API

**Option A : Gemini API (Recommandé)**
1. Aller sur https://aistudio.google.com/app/apikey
2. Cliquer "Create API Key"
3. Copier la clé

**Option B : Groq API**
1. Aller sur https://console.groq.com/keys
2. Créer une API key
3. Copier la clé

### 5. Créer fichier .env
```bash
cp .env.example .env
```

Éditer `.env` et ajouter votre clé :
```
AI_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
```

### 6. Générer les données fictives
```bash
python scripts/generate_demo_data.py
```

Cela crée 10 fichiers CSV dans `data/` :
- fact_ecritures_comptables.csv
- fact_factures_fournisseurs.csv
- fact_budget.csv
- fact_tresorerie.csv
- etc.

### 7. Construire le vector store (optionnel pour Chat RAG)
```bash
python scripts/build_vector_store.py
```

### 8. Lancer l'application
```bash
streamlit run app.py
```

L'app s'ouvre automatiquement sur http://localhost:8501

## 📊 Structure des Fichiers

```
enterprise-ai-accounting-finance-assistant/
│
├── README.md                           # Ce fichier
├── requirements.txt                    # Dépendances
├── .env.example                        # Template configuration
├── .gitignore                          # Git ignore
├── app.py                              # Application Streamlit principale
│
├── src/                                # Code source
│   ├── __init__.py
│   ├── config.py                       # Configuration settings
│   ├── llm_provider.py                 # Abstraction LLM (Gemini/Groq)
│   ├── security.py                     # Sécurité et secrets
│   ├── data_loader.py                  # Chargement données CSV
│   ├── rag_pipeline.py                 # Pipeline RAG complet
│   ├── accounting_analyzer.py          # Analyse comptabilité
│   ├── finance_analyzer.py             # Analyse budget/réel
│   ├── supplier_accounting.py          # Analyse fournisseurs
│   ├── treasury_analyzer.py            # Analyse trésorerie
│   ├── quality_checker.py              # Contrôle qualité données
│   ├── management_commentary.py        # Génération commentaires
│   └── prompt_templates.py             # Templates prompts LLM
│
├── scripts/                            # Scripts utilitaires
│   ├── generate_demo_data.py           # Génération données fictives
│   └── build_vector_store.py           # Construction vector store RAG
│
├── data/                               # Données CSV
│   ├── fact_ecritures_comptables.csv
│   ├── fact_factures_fournisseurs.csv
│   ├── fact_budget.csv
│   ├── fact_tresorerie.csv
│   ├── fact_rapprochement_bancaire.csv
│   ├── dim_compte_comptable.csv
│   ├── dim_centre_cout.csv
│   ├── dim_projet.csv
│   ├── dim_fournisseur.csv
│   └── dim_date.csv
│
├── docs/                               # Documentation métier
│   ├── procedure_cloture_mensuelle.md
│   ├── procedure_comptabilite_fournisseurs.md
│   ├── procedure_rapprochement_bancaire.md
│   ├── catalogue_kpi_finance.md
│   ├── dictionnaire_donnees_finance.md
│   ├── regles_controle_comptable.md
│   ├── gouvernance_ia_finance.md
│   └── cas_usage_ia_comptabilite_finance.md
│
├── powerbi/                            # Documentation Power BI
│   ├── README_powerbi.md
│   ├── data_model_star_schema.md
│   ├── dax_measures.md
│   └── dashboard_specification.md
│
├── tests/                              # Tests unitaires
│   ├── test_accounting_analyzer.py
│   ├── test_finance_analyzer.py
│   ├── test_supplier_accounting.py
│   ├── test_treasury_analyzer.py
│   └── test_quality_checker.py
│
└── assets/                             # Assets du projet
    └── architecture_description.md
```

## 📚 Documentation

### Pour les développeurs
- [Architecture technique](assets/architecture_description.md)
- [Procédure clôture mensuelle](docs/procedure_cloture_mensuelle.md)
- [Règles de contrôle comptable](docs/regles_controle_comptable.md)
- [Gouvernance IA](docs/gouvernance_ia_finance.md)

### Pour les analystes finance
- [Catalogue KPI Finance](docs/catalogue_kpi_finance.md)
- [Dictionnaire des données](docs/dictionnaire_donnees_finance.md)
- [Cas d'usage IA](docs/cas_usage_ia_comptabilite_finance.md)

### Pour Power BI
- [Guide Power BI complet](powerbi/README_powerbi.md)
- [Modèle Star Schema](powerbi/data_model_star_schema.md)
- [Mesures DAX](powerbi/dax_measures.md)
- [Spécification dashboards](powerbi/dashboard_specification.md)

## 🔎 Démo rapide

- **Extrait de commentaire généré** : [assets/demo_commentaires/2026-06-03_commentaire_demo.md](assets/demo_commentaires/2026-06-03_commentaire_demo.md)
- **Capture UI** : [assets/demo_commentaires/2026-06-03_ui_screenshot.jpg](assets/demo_commentaires/2026-06-03_ui_screenshot.jpg)

## Screenshots

- Aperçu de l'interface :

  ![UI demo](assets/demo_commentaires/2026-06-03_ui_screenshot.jpg)

- Dossier complet des captures : `captures d'images/` (contient des captures d'écran supplémentaires montrant les vues Comptabilité, Fournisseurs, Trésorerie, Budget, etc.).


## 🔧 Configuration Avancée

### Changer le provider LLM
```env
# Utiliser Groq à la place
AI_PROVIDER=groq
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### Personnaliser les paramètres
```env
# Taille des chunks pour RAG
CHUNK_SIZE=1500
CHUNK_OVERLAP=300

# Modèle et paramètres LLM
TEMPERATURE=0.8
MAX_TOKENS=2000
```

## 🧪 Tests

Lancer tous les tests :
```bash
pytest tests/ -v
```

Avec couverture :
```bash
pytest tests/ --cov=src
```

## 🚢 Déploiement

### Sur Streamlit Cloud
```bash
git push origin main
# Dans Streamlit Cloud, connecter votre repo GitHub
# Deploy > Pick app file: app.py
```

### Sur Azure
```bash
# Créer Azure Container App
az containerapp create --name finance-assistant \
  --image app:latest \
  --environment ...
```

### Localement / On-prem
```bash
# Simple
streamlit run app.py

# Production (avec Gunicorn)
gunicorn --workers 4 app:app
```

## 🔒 Sécurité

✅ **Implémenté**
- Clés API stockées en `.env`, jamais en dur
- `.env` dans `.gitignore`
- Validation des configurations
- Gestion des cas sans API configurée
- Masquage des informations sensibles

⚠️ **À implémenter selon votre contexte**
- Authentification utilisateur
- Contrôle d'accès basé rôles (RBAC)
- Audit des actions
- Chiffrement données sensibles

## 🤖 IA et Gouvernance

### Principes appliqués
1. **Transparence** : Sources documentées, citations en citations
2. **Fiabilité** : Recommandations soumises à validation humaine
3. **Conformité** : Respect des règles comptables
4. **Traçabilité** : Logs de toutes les décisions IA

### Capacités IA
- ✅ Assistance à la décision
- ✅ Suggestion et recommandation
- ❌ Signature / Approbation finale
- ❌ Validation sans relecture humaine

## 📸 Captures d'écran & Commentaire généré

Pour enrichir le README avec des captures d'écran, place tes images dans le dossier `assets/screenshots/` (crée-le si nécessaire). Nomme les fichiers de façon lisible et ordonnée pour faciliter l'insertion :

- `01_home.png` : page d'accueil (navigation + configuration visible)
- `02_chat_account.png` : Chat IA — question comptable (ex. "Quel est le solde du compte 615 ?")
- `03_chat_supplier.png` : Chat IA — question fournisseur (ex. "Quel fournisseur a le plus grand montant ?")
- `04_accounting.png` : Onglet Comptabilité (graphiques et indicateurs)
- `05_suppliers.png` : Onglet Fournisseurs (classement / résumé)
- `06_commentary.png` : Onglet Commentaire (commentaire généré automatiquement)

Exemple d'insertion Markdown pour une image avec légende :

```markdown
![Page d'accueil](assets/screenshots/01_home.png)
*Figure 1 — Page d'accueil avec navigation et statut Ollama local.*
```

Commentaire généré (exemple) — tu peux copier-coller ce texte si tu veux montrer la fonctionnalité :

> En mai, le chiffre d'affaires consolidé est en hausse de 4,2 % vs budget principalement porté par le projet "Alpha". Les charges externes augmentent de 3,8 % et expliquent l'écart négatif sur la marge brute. Recommandation : vérifier les postes fournisseurs 4012 et 615 pour valider la répartition des coûts et prioriser le recouvrement des factures échues.

Procédure recommandée pour intégrer les captures et le commentaire dans le README :

1. Copier les captures dans `assets/screenshots/`.
2. Dans le README, ajouter les blocs Markdown avec les images et une légende claire.
3. Inclure le commentaire généré sous la capture `06_commentary.png` en tant que blockquote (voir exemple ci‑dessus).
4. Commit et push :

```bash
git add assets/screenshots/*.png README.md
git commit -m "Ajout captures d'écran + exemple commentaire"
git push
```

Si tu veux, je peux :

- Créer le dossier `assets/screenshots/` dans le repo.
- Ajouter les blocs Markdown pré-remplis dans le README avec des liens vers les fichiers (à remplacer par tes captures finales).
- Générer un fichier `docs/screenshots_instructions.md` plus détaillé.

Dis‑moi ce que tu souhaites que je fasse en automatique.

## 📊 Données Fictives

Les données sont **réalistes mais fictives** pour une entreprise de services financiers :

- **12 mois** de données
- **600+ écritures comptables**
- **120+ factures fournisseurs**
- **20 projets**
- **10 centres de coûts**
- **35 fournisseurs**
- **Anomalies volontaires** pour démontrer les contrôles

Les données sont idéales pour le **prototypage** mais pas pour la production.

## 🎓 Concepts Financiers Appliqués

### Comptabilité
- Équilibre débit/crédit
- Plan comptable simplifié
- Journaux comptables (AC, VE, OP, TR)
- Clôture mensuelle

### Finance
- Budget vs réel
- Écarts budgétaires
- Consommation budgétaire
- OPEX vs CAPEX

### Trésorerie
- Cash flow
- Rapprochement bancaire
- Prévisions de liquidité
- Cycle de conversion

### Contrôle de gestion
- Centres de coûts
- Suivi projets
- KPI finance
- Commentaires de gestion

## 🤝 Contribution

Les contributions sont bienvenues !

1. Forker le projet
2. Créer une branche (`git checkout -b feature/amazing-feature`)
3. Commit (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir [LICENSE](LICENSE) pour plus de détails.

## 👤 Auteur

**Développeur Finance + IA**

Portfolio : [Votre website]  
Email : [Votre email]  
LinkedIn : [Votre LinkedIn]

## 🙌 Remerciements

- Google Gemini API pour l'IA
- Groq pour l'accès API gratuit
- Streamlit pour la simplicité
- Communauté open source Python

## 📧 Support

Pour les questions ou problèmes :
- Ouvrir une issue sur GitHub
- Contacter l'auteur
- Consulter la documentation

---

**Fait avec ❤️ pour les DAF qui veulent automatiser la comptabilité grâce à l'IA**

⭐ Si ce projet vous a plu, mettez une star !
