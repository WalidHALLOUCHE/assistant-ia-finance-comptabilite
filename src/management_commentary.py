"""Generate management commentary on financial performance."""

import pandas as pd
from typing import Optional
# Import LLM provider lazily to avoid requiring Ollama/config at module import time
from src.prompt_templates import MANAGEMENT_COMMENTARY_PROMPT


class ManagementCommentaryGenerator:
    """Generate management commentary using LLM or rules."""

    def __init__(self):
        """Initialize generator."""
        self.llm_available = False
        try:
            from src.llm_provider import LLMProvider as _LLMProvider
            self.llm_available = _LLMProvider.is_api_available()
            if self.llm_available:
                try:
                    self.provider = _LLMProvider()
                    self.model = self.provider.get_chat_model()
                except Exception:
                    self.llm_available = False
        except Exception:
            # Ollama/LLM provider not available or import failed; continue with rules
            self.llm_available = False

    def generate_commentary(
        self,
        financial_summary: dict,
        budget_analysis: dict,
        issues: list,
        use_llm: bool = True,
    ) -> str:
        """Generate management commentary."""
        if use_llm and self.llm_available:
            return self._generate_with_llm(financial_summary, budget_analysis, issues)
        else:
            return self._generate_with_rules(financial_summary, budget_analysis, issues)

    def _generate_with_llm(self, financial_summary: dict, budget_analysis: dict, issues: list) -> str:
        """Generate commentary using LLM."""
        try:
            prompt = MANAGEMENT_COMMENTARY_PROMPT.format(
                financial_data=str(financial_summary),
                budget_analysis=str(budget_analysis),
                issues=str(issues),
            )

            response = self.model.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Error generating commentary: {e}. Falling back to rules-based approach."

    def _generate_with_rules(self, financial_summary: dict, budget_analysis: dict, issues: list) -> str:
        """Generate commentary using rules (no LLM)."""
        sections = []

        # Performance section
        sections.append(self._build_performance_section(financial_summary, budget_analysis))

        # Budget analysis section
        sections.append(self._build_budget_section(budget_analysis))

        # Issues section
        if issues:
            sections.append(self._build_issues_section(issues))

        # Recommendations
        sections.append(self._build_recommendations_section(financial_summary, budget_analysis))

        return "\n\n".join(sections)

    def _build_performance_section(self, financial_summary: dict, budget_analysis: dict) -> str:
        """Build performance commentary."""
        # budget_analysis may be a dict, list of dicts, or a pandas DataFrame
        try:
            if isinstance(budget_analysis, list):
                records = budget_analysis
            elif isinstance(budget_analysis, pd.DataFrame):
                records = budget_analysis.to_dict("records")
            elif isinstance(budget_analysis, dict):
                records = None
            else:
                # Fallback: try to treat as mapping-like
                records = None

            if records is not None:
                total_budget = sum([x.get("budget", 0) for x in records])
                total_reel = sum([x.get("reel", 0) for x in records])
                total_variance = total_reel - total_budget
                budget_consumed = round((total_reel / total_budget * 100) if total_budget else 0, 2)
                variance = round((total_variance / total_budget * 100) if total_budget else 0, 2)
            else:
                # Expect a dict-like object
                if isinstance(budget_analysis, dict):
                    budget_consumed = budget_analysis.get("budget_consumed_percent", 0)
                    variance = budget_analysis.get("variance_percent", 0)
                else:
                    # Unknown type: safe defaults
                    budget_consumed = 0
                    variance = 0
        except Exception:
            budget_consumed = 0
            variance = 0

        section = "**SYNTHÈSE DE PERFORMANCE FINANCIÈRE\n"
        section += f"\nLe budget a été consommé à {budget_consumed:.1f}% de la prévision annuelle.\n"

        if variance > 10:
            section += f"Les dépenses réelles dépassent le budget de {variance:.1f}%, "
            section += "indiquant une dérive significative des charges.\n"
        elif variance < -10:
            section += f"Les dépenses réelles sont inférieures au budget de {abs(variance):.1f}%, "
            section += "montrant une bonne maîtrise des coûts.\n"
        else:
            section += "Les dépenses restent dans les limites budgétaires acceptables.\n"

        return section

    def _build_budget_section(self, budget_analysis: dict) -> str:
        """Build budget analysis commentary."""
        section = "**ANALYSE BUDGÉTAIRE\n"

        # Accept either dict or list of dicts
        if isinstance(budget_analysis, list):
            total_budget = sum([x.get("budget", 0) for x in budget_analysis])
            total_reel = sum([x.get("reel", 0) for x in budget_analysis])
            total_variance = total_reel - total_budget
        else:
            total_variance = budget_analysis.get("total_variance", 0)

        if total_variance > 0:
            section += f"Écart positif (dépassement) : {abs(total_variance):,.2f} €\n"
        else:
            section += f"Écart négatif (économie) : {abs(total_variance):,.2f} €\n"

        section += "Les centres de coûts principaux doivent être examinés en détail.\n"

        return section

    def _build_issues_section(self, issues: list) -> str:
        """Build issues commentary."""
        section = "**POINTS D'ATTENTION\n"

        if not issues:
            section += "Aucun problème significatif détecté.\n"
        else:
            for idx, issue in enumerate(issues[:3], 1):
                if isinstance(issue, dict):
                    section += f"\n{idx}. {issue.get('description', 'Problème identifié')}\n"
                else:
                    section += f"\n{idx}. {str(issue)}\n"

        return section

    def _build_recommendations_section(self, financial_summary: dict, budget_analysis: dict) -> str:
        """Build recommendations."""
        section = "**RECOMMANDATIONS\n"

        # Normalize budget_analysis: accept dict or list of dicts
        try:
            if isinstance(budget_analysis, list):
                total_budget = sum([x.get("budget", 0) for x in budget_analysis])
                total_reel = sum([x.get("reel", 0) for x in budget_analysis])
                variance_percent = round(((total_reel - total_budget) / total_budget * 100) if total_budget else 0, 2)
            else:
                variance_percent = budget_analysis.get("variance_percent", 0)
        except Exception:
            variance_percent = 0

        if variance_percent > 15:
            section += "- Audit des postes de dépenses majeurs recommandé\n"

        section += "- Suivi hebdomadaire des écarts recommandé\n"
        section += "- Révision des prévisions si dépassement confirmé\n"

        return section
