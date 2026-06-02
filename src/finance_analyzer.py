"""Finance and budget analysis."""

import pandas as pd
from typing import Dict
import numpy as np


class FinanceAnalyzer:
    """Analyze financial performance and budgets."""

    def __init__(self, budget_df: pd.DataFrame, ecritures_df: pd.DataFrame):
        """Initialize analyzer."""
        self.budget_df = budget_df.copy()
        self.ecritures_df = ecritures_df.copy()
        self._prepare_data()

    def _prepare_data(self):
        """Prepare data for analysis."""
        self.budget_df["budget"] = pd.to_numeric(self.budget_df["budget"], errors="coerce")
        self.budget_df["reel"] = pd.to_numeric(self.budget_df["reel"], errors="coerce")
        self.budget_df["ecart"] = pd.to_numeric(self.budget_df["ecart"], errors="coerce")

    def get_budget_summary(self) -> Dict:
        """Get overall budget summary."""
        total_budget = self.budget_df["budget"].sum()
        total_real = self.budget_df["reel"].sum()
        total_variance = total_real - total_budget

        return {
            "total_budget": round(total_budget, 2),
            "total_real": round(total_real, 2),
            "total_variance": round(total_variance, 2),
            "variance_percent": round((total_variance / total_budget * 100) if total_budget > 0 else 0, 2),
            "budget_consumed_percent": round((total_real / total_budget * 100) if total_budget > 0 else 0, 2),
        }

    def get_cost_center_analysis(self) -> pd.DataFrame:
        """Analyze budget by cost center."""
        analysis = (
            self.budget_df.groupby("centre_cout")[["budget", "reel", "ecart"]]
            .sum()
            .reset_index()
        )

        analysis["variance_percent"] = (
            (analysis["ecart"] / analysis["budget"] * 100)
            .fillna(0)
            .round(2)
        )
        analysis["budget_consumed_percent"] = (
            (analysis["reel"] / analysis["budget"] * 100)
            .fillna(0)
            .round(2)
        )

        return analysis.sort_values("variance_percent", ascending=False)

    def get_top_variances(self, top_n: int = 10, variance_type: str = "positive") -> pd.DataFrame:
        """Get top budget variances."""
        df = self.budget_df.copy()

        if variance_type == "positive":
            df = df[df["ecart"] < 0].sort_values("ecart")
        else:  # negative (over budget)
            df = df[df["ecart"] > 0].sort_values("ecart", ascending=False)

        return df.head(top_n)

    def get_projects_overbudget(self) -> pd.DataFrame:
        """Get projects that are over budget."""
        # This would need project-level budget data
        # For now, return empty as it's in supplier accounting
        return pd.DataFrame()

    def get_monthly_budget_trend(self) -> pd.DataFrame:
        """Get budget vs real by month."""
        trend = (
            self.budget_df.groupby("mois")[["budget", "reel"]]
            .sum()
            .reset_index()
        )

        trend["variance"] = trend["reel"] - trend["budget"]
        trend["variance_percent"] = (
            (trend["variance"] / trend["budget"] * 100)
            .fillna(0)
            .round(2)
        )

        return trend

    def analyze_opex_capex(self) -> Dict:
        """Analyze OPEX vs CAPEX if categorized."""
        # This would require classification in the data
        # Placeholder implementation
        return {
            "opex_budget": 0,
            "opex_real": 0,
            "capex_budget": 0,
            "capex_real": 0,
        }

    def get_budget_consumption_rate(self) -> float:
        """Get percentage of budget consumed."""
        summary = self.get_budget_summary()
        return summary["budget_consumed_percent"]

    def is_on_track(self, tolerance_percent: float = 10) -> bool:
        """Check if budget is on track (within tolerance)."""
        summary = self.get_budget_summary()
        variance_percent = abs(summary["variance_percent"])
        return bool(variance_percent <= tolerance_percent)
