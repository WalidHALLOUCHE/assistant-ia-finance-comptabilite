"""
Enterprise AI Accounting & Finance Assistant - Streamlit Application
Main entry point for the web application.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import re
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import settings
from src.data_loader import DataLoader
from src.accounting_analyzer import AccountingAnalyzer
from src.finance_analyzer import FinanceAnalyzer
from src.supplier_accounting import SupplierAccountingAnalyzer
from src.treasury_analyzer import TreasuryAnalyzer
from src.quality_checker import QualityChecker
from src.management_commentary import ManagementCommentaryGenerator
from src.llm_provider import LLMProvider

# Optional RAG pipeline (requires langchain and chromadb)
RAG_AVAILABLE = False
try:
    from src.rag_pipeline import RAGPipeline
    RAG_AVAILABLE = True
except ImportError:
    RAGPipeline = None


# Page configuration
st.set_page_config(
    page_title="Assistant IA Comptabilité & Finance",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0068c9;
    }
    .critical-alert {
        background-color: #ffcccc;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff0000;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_data():
    """Load and cache all data."""
    try:
        loader = DataLoader()
        return loader.load_all_data()
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données: {e}")
        return None


@st.cache_resource
def initialize_analyzers(data):
    """Initialize all analyzers."""
    if data is None:
        return None
    
    return {
        "accounting": AccountingAnalyzer(
            data["ecritures_comptables"],
            data["compte_comptable"]
        ),
        "finance": FinanceAnalyzer(data["budget"], data["ecritures_comptables"]),
        "supplier": SupplierAccountingAnalyzer(
            data["factures_fournisseurs"],
            data["fournisseur"]
        ),
        "treasury": TreasuryAnalyzer(
            data["tresorerie"],
            data["rapprochement_bancaire"]
        ),
        "quality": QualityChecker(data),
    }


def render_home():
    """Render home page."""
    st.markdown("# 🏛️ Assistant IA Comptabilité & Finance")
    st.markdown("**Bienvenue** dans l'assistant IA pour la comptabilité, la finance et le contrôle de gestion.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        ### 📋 Fonctionnalités
        - ✅ Analyse comptabilité générale
        - ✅ Suivi comptabilité fournisseurs
        - ✅ Gestion trésorerie
        - ✅ Contrôle budgétaire
        - ✅ Détection anomalies
        - ✅ Génération commentaires
        - ✅ Chat IA avec RAG
        """)
    
    with col2:
        st.warning("""
        ### ⚙️ Configuration
        """)
        
        # Check API configuration
        is_valid, message = settings.validate_ai_configuration()
        if is_valid:
            st.success(message)
        else:
            st.error(message)
        
        # Show provider info
        provider_info = LLMProvider.get_provider_info()
        st.json(provider_info)
    
    # Data info
    st.markdown("### 📊 Données")
    col1, col2, col3 = st.columns(3)
    
    data = load_data()
    if data:
        col1.metric("📝 Écritures comptables", len(data["ecritures_comptables"]))
        col2.metric("💳 Factures fournisseurs", len(data["factures_fournisseurs"]))
        col3.metric("📊 Projets", len(data["projet"]))
    
    # Description
    st.markdown("""
    ### À propos du projet
    
    Assistant IA pour la comptabilité, finance et contrôle de gestion:
    
    - **100% Open-Source**: Ollama (local, sans dépendances propriétaires)
    - **Connaissance métier**: Intègre procédures via RAG
    - **Données temps réel**: Connecté aux données financières
    - **Gouvernance**: Architecture prête pour déploiement entreprise
    - **Flexible**: Adaptable à tous secteurs d'activité
    
    #### Technologies
    - **Frontend**: Streamlit
    - **LLM**: Ollama (open-source, local)
    - **Embeddings**: Nomic Embed Text (open-source)
    - **RAG**: ChromaDB + LangChain
    - **Analytics**: Pandas, Plotly
    - **Données**: Fictives, universelles et réalistes
    """)


def render_chat():
    """Render AI Chat page."""
    st.markdown("# 💬 Assistant IA Comptabilité & Finance")
    
    # Check if RAG is available
    if not RAG_AVAILABLE:
        st.warning("⚠️ Le pipeline RAG n'est pas disponible.")
        st.info("""
        Pour activer la fonctionnalité Chat IA avec analyse documentaire, installez les dépendances optionnelles:
        ```bash
        pip install langchain chromadb
        python scripts/build_vector_store.py
        ```
        """)
        return
    
    # Check if LLM is configured
    is_valid, message = settings.validate_ai_configuration()
    if not is_valid:
        st.error(message)
        return
    
    # Initialize RAG pipeline
    rag = RAGPipeline()
    
    if not rag.is_ready():
        st.warning("⚠️  Le pipeline RAG n'est pas prêt. Veuillez construire le vector store d'abord.")
        st.code("python scripts/build_vector_store.py", language="bash")
        return
    
    # Available topics
    topics = rag.get_available_topics()
    if topics:
        st.markdown(f"**Sujets disponibles**: {', '.join(topics[:5])}...")

    data = load_data()
    analyzers = initialize_analyzers(data) if data is not None else None

    def _answer_data_question(question: str):
        """Return a direct answer for simple account questions based on loaded data."""
        if not analyzers:
            return None

        normalized_question = question.lower()

        match = re.search(r"compte\s*(\d{3,4})", question, flags=re.IGNORECASE)
        if match:
            account = match.group(1)
            balances = analyzers["accounting"].get_account_balances()
            row = balances[balances["compte"].astype(str) == account]
            if row.empty:
                return f"Je n'ai pas trouvé le compte {account} dans les données chargées.", ["données comptables"]

            debit = float(row.iloc[0]["debit"])
            credit = float(row.iloc[0]["credit"])
            solde = float(row.iloc[0]["solde"])

            answer = (
                f"Le compte {account} a un débit total de €{debit:,.2f}, un crédit total de €{credit:,.2f} "
                f"et un solde de €{solde:,.2f}."
            )
            return answer, ["données comptables"]

        if (
            "fournisseur" in normalized_question
            and any(term in normalized_question for term in ["plus grand", "plus gros", "max", "maximum", "top"])
        ):
            supplier_analyzer = analyzers["supplier"]
            top_suppliers = supplier_analyzer.get_top_suppliers(1)
            if top_suppliers.empty:
                return "Je n'ai trouvé aucune facture fournisseur dans les données chargées.", ["données fournisseurs"]

            supplier_name = top_suppliers.iloc[0]["fournisseur_nom"]
            supplier_amount = float(top_suppliers.iloc[0]["total_amount"])
            answer = f"Le fournisseur avec le plus grand montant est {supplier_name} avec un total de €{supplier_amount:,.2f}."
            return answer, ["données fournisseurs"]

        return None
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message and message["sources"]:
                st.caption(f"📚 Sources: {', '.join(message['sources'])}")
    
    # Input
    if prompt := st.chat_input("Posez une question sur la comptabilité et la finance..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("🤔 Réflexion..."):
                direct_answer = _answer_data_question(prompt)
                if direct_answer is not None:
                    answer, sources = direct_answer
                else:
                    answer, sources = rag.query(prompt)
                st.markdown(answer)
                if sources:
                    st.caption(f"📚 Sources: {', '.join(sources)}")
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources
        })


def render_accounting():
    """Render accounting page."""
    st.markdown("# 📝 Comptabilité Générale")
    
    data = load_data()
    if data is None:
        return
    
    analyzers = initialize_analyzers(data)
    if analyzers is None:
        return
    
    accounting = analyzers["accounting"]
    
    # Summary
    col1, col2, col3, col4 = st.columns(4)
    summary = accounting.get_balance_sheet_summary()
    col1.metric("Total Débits", f"€{summary['total_debit']:,.2f}")
    col2.metric("Total Crédits", f"€{summary['total_credit']:,.2f}")
    col3.metric("Solde", f"€{summary['difference']:,.2f}")
    col4.metric("Équilibré", "✅ Oui" if summary["is_balanced"] else "❌ Non")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Balance", "Anomalies", "Tendances", "Qualité"])
    
    with tab1:
        st.markdown("### Balance Comptable")
        balances = accounting.get_account_balances()
        st.dataframe(
            balances,
            use_container_width=True,
            hide_index=True
        )
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Écritures non équilibrées")
            unbalanced = accounting.get_unbalanced_entries()
            st.metric("Nombre", len(unbalanced))
            if len(unbalanced) > 0:
                st.dataframe(unbalanced[["ecriture_id", "montant", "libelle"]], use_container_width=True)
        
        with col2:
            st.markdown("#### Écritures sans centre de coût")
            missing_cc = accounting.get_entries_missing_cost_center()
            st.metric("Nombre", len(missing_cc))
    
    with tab3:
        st.markdown("### Tendances mensuelles")
        monthly = accounting.get_monthly_summary()
        if len(monthly) > 0:
            fig = px.line(
                monthly,
                x="month",
                y="total_amount",
                title="Montant par mois",
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### Qualité des données")
        anomalies = accounting.detect_anomalies()
        for key, value in anomalies.items():
            st.metric(key.replace("_", " ").title(), value)


def render_supplier():
    """Render supplier accounting page."""
    st.markdown("# 💳 Comptabilité Fournisseurs")
    
    data = load_data()
    if data is None:
        return
    
    analyzers = initialize_analyzers(data)
    if analyzers is None:
        return
    
    supplier = analyzers["supplier"]
    
    # Summary
    summary = supplier.get_summary()
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Factures", summary["total_invoices"])
    col2.metric("Montant Total", f"€{summary['total_amount']:,.0f}")
    col3.metric("Payées", summary["paid_invoices"])
    col4.metric("Échues", summary["overdue_invoices"])
    col5.metric("Montant Échues", f"€{summary['overdue_amount']:,.0f}")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Fournisseurs", "Factures", "Risque", "Tendances"])
    
    with tab1:
        st.markdown("### Top 10 Fournisseurs")
        top_suppliers = supplier.get_top_suppliers(10)
        fig = px.bar(
            top_suppliers,
            x="total_amount",
            y="fournisseur_nom",
            orientation="h",
            title="Montant par fournisseur"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Factures par statut")
        by_status = supplier.get_invoices_by_status()
        fig = px.pie(
            by_status,
            values="amount",
            names="statut",
            title="Répartition par statut"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Factures échues")
        overdue = supplier.get_overdue_invoices()
        if len(overdue) > 0:
            st.dataframe(
                overdue[["facture_id", "fournisseur_id", "montant_ttc", "date_echeance"]],
                use_container_width=True
            )
        else:
            st.success("✅ Aucune facture échue")
    
    with tab4:
        st.markdown("### Délai moyen de paiement")
        perf = supplier.get_payment_performance_by_supplier()
        if len(perf) > 0:
            fig = px.bar(
                perf.head(10),
                x="avg_payment_days",
                y="fournisseur_nom",
                orientation="h",
                title="Délai moyen par fournisseur"
            )
            st.plotly_chart(fig, use_container_width=True)


def render_treasury():
    """Render treasury page."""
    st.markdown("# 💰 Trésorerie")
    
    data = load_data()
    if data is None:
        return
    
    analyzers = initialize_analyzers(data)
    if analyzers is None:
        return
    
    treasury = analyzers["treasury"]
    
    # Summary
    summary = treasury.get_treasury_summary()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Solde Actuel", f"€{summary['current_cash']:,.0f}")
    col2.metric("Cash In", f"€{summary['total_cash_in']:,.0f}")
    col3.metric("Cash Out", f"€{summary['total_cash_out']:,.0f}")
    col4.metric("Solde Moyen", f"€{summary['average_daily_balance']:,.0f}")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Évolution", "Rapprochement", "Prévision"])
    
    with tab1:
        st.markdown("### Évolution du solde de trésorerie")
        daily = treasury.get_daily_cash_flow()
        fig = px.line(
            daily,
            x="date",
            y="solde",
            title="Solde de trésorerie",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Rapprochement bancaire")
        recon_summary = treasury.get_reconciliation_summary()
        col1, col2, col3 = st.columns(3)
        col1.metric("Mouvements", recon_summary["total_movements"])
        col2.metric("Rapprochés", recon_summary["reconciled"])
        col3.metric("Taux", f"{recon_summary['reconciliation_rate_percent']:.1f}%")
        
        unreconciled = treasury.get_unreconciled_movements()
        if len(unreconciled) > 0:
            st.warning(f"⚠️  {len(unreconciled)} mouvements non rapprochés")
            st.dataframe(unreconciled, use_container_width=True)
    
    with tab3:
        st.markdown("### Prévision de trésorerie")
        forecast = treasury.forecast_liquidity(30)
        col1, col2 = st.columns(2)
        col1.metric("Solde Actuel", f"€{forecast.get('current_cash', 0):,.0f}")
        col2.metric("Prévision +30j", f"€{forecast.get('forecast_30d', 0):,.0f}")


def render_budget():
    """Render budget page."""
    st.markdown("# 📊 Contrôle de Gestion")
    
    data = load_data()
    if data is None:
        return
    
    analyzers = initialize_analyzers(data)
    if analyzers is None:
        return
    
    finance = analyzers["finance"]
    
    # Summary
    summary = finance.get_budget_summary()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Budget", f"€{summary['total_budget']:,.0f}")
    col2.metric("Réel", f"€{summary['total_real']:,.0f}")
    col3.metric("Écart", f"€{summary['total_variance']:,.0f}")
    col4.metric("Écart %", f"{summary['variance_percent']:.1f}%")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Par centre", "Tendances", "Détail"])
    
    with tab1:
        st.markdown("### Budget vs Réel par centre de coût")
        by_center = finance.get_cost_center_analysis()
        fig = px.bar(
            by_center,
            x="centre_cout",
            y=["budget", "reel"],
            barmode="group",
            title="Budget vs Réel"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Tendances mensuelles")
        trend = finance.get_monthly_budget_trend()
        fig = px.line(
            trend,
            x="mois",
            y=["budget", "reel"],
            title="Budget vs Réel par mois",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Détail des écarts")
        variances = finance.get_top_variances(20)
        st.dataframe(variances, use_container_width=True)


def render_quality():
    """Render data quality page."""
    st.markdown("# ✅ Qualité des Données")
    
    data = load_data()
    if data is None:
        return
    
    analyzers = initialize_analyzers(data)
    if analyzers is None:
        return
    
    quality = analyzers["quality"]
    total_issues, score, issues = quality.run_all_checks()
    
    # Summary
    col1, col2, col3 = st.columns(3)
    col1.metric("Score Qualité", f"{score}%")
    col2.metric("Anomalies", total_issues)
    col3.metric("Statut", "🟢 Bon" if score >= 90 else "🟡 Acceptable" if score >= 80 else "🔴 À améliorer")
    
    # Tabs
    tab1, tab2 = st.tabs(["Anomalies", "Recommandations"])
    
    with tab1:
        st.markdown("### Anomalies détectées")
        if issues:
            issues_df = pd.DataFrame(issues)
            fig = px.bar(
                issues_df,
                x="type",
                y="count",
                color="severity",
                title="Anomalies par type"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(issues_df, use_container_width=True)
        else:
            st.success("✅ Aucune anomalie détectée")
    
    with tab2:
        st.markdown("### Recommandations")
        recommendations = quality.get_recommendations()
        for rec in recommendations:
            st.info(rec)


def render_commentary():
    """Render management commentary page."""
    st.markdown("# 📄 Commentaire de Gestion")
    
    data = load_data()
    if data is None:
        return
    
    analyzers = initialize_analyzers(data)
    if analyzers is None:
        return
    
    # Generate commentary
    generator = ManagementCommentaryGenerator()
    
    finance = analyzers["finance"]
    quality = analyzers["quality"]
    
    financial_summary = finance.get_budget_summary()
    budget_analysis = finance.get_cost_center_analysis().to_dict("records")
    _, _, issues = quality.run_all_checks()
    
    # Allow user to choose whether to use the local Ollama LLM (may be slow)
    use_llm = st.checkbox("Utiliser Ollama local pour générer le commentaire (peut être lent)", value=False)

    with st.spinner("📝 Génération du commentaire..."):
        commentary = generator.generate_commentary(
            financial_summary,
            budget_analysis,
            issues,
            use_llm=use_llm,
        )
    
    st.markdown(commentary)
    
    # Download option
    st.download_button(
        label="📥 Télécharger en Markdown",
        data=commentary,
        file_name=f"commentaire_gestion_{datetime.now().strftime('%Y%m%d')}.md",
        mime="text/markdown"
    )


def main():
    """Main application."""
    # Sidebar navigation
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/accounting.png", width=80)
        st.markdown("# 🏛️ Finance IA")
        
        page = st.radio(
            "Navigation",
            [
                "🏠 Accueil",
                "💬 Chat IA",
                "📝 Comptabilité",
                "💳 Fournisseurs",
                "💰 Trésorerie",
                "📊 Budget",
                "✅ Qualité",
                "📄 Commentaire"
            ]
        )
        
        st.markdown("---")
        st.markdown("### ⚙️ Configuration")
        
        # Check API
        is_valid, message = settings.validate_ai_configuration()
        if is_valid:
            st.success("✅ Ollama local configuré")
        else:
            st.error("❌ Ollama local non configuré")
    
    # Page routing
    if page == "🏠 Accueil":
        render_home()
    elif page == "💬 Chat IA":
        render_chat()
    elif page == "📝 Comptabilité":
        render_accounting()
    elif page == "💳 Fournisseurs":
        render_supplier()
    elif page == "💰 Trésorerie":
        render_treasury()
    elif page == "📊 Budget":
        render_budget()
    elif page == "✅ Qualité":
        render_quality()
    elif page == "📄 Commentaire":
        render_commentary()


if __name__ == "__main__":
    main()
