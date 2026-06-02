"""Treasury and cash flow analysis."""

import pandas as pd
from typing import Dict


class TreasuryAnalyzer:
    """Analyze treasury and cash flow."""

    def __init__(self, tresorerie_df: pd.DataFrame, rapprochement_df: pd.DataFrame):
        """Initialize analyzer."""
        self.tresorerie_df = tresorerie_df.copy()
        self.rapprochement_df = rapprochement_df.copy()
        self._prepare_data()

    def _prepare_data(self):
        """Prepare data for analysis."""
        self.tresorerie_df["date"] = pd.to_datetime(self.tresorerie_df["date"], errors="coerce")
        self.tresorerie_df["cash_in"] = pd.to_numeric(self.tresorerie_df["cash_in"], errors="coerce")
        self.tresorerie_df["cash_out"] = pd.to_numeric(self.tresorerie_df["cash_out"], errors="coerce")
        self.tresorerie_df["solde"] = pd.to_numeric(self.tresorerie_df["solde"], errors="coerce")

    def get_treasury_summary(self) -> Dict:
        """Get treasury summary."""
        return {
            "current_cash": round(self.tresorerie_df["solde"].iloc[-1] if len(self.tresorerie_df) > 0 else 0, 2),
            "total_cash_in": round(self.tresorerie_df["cash_in"].sum(), 2),
            "total_cash_out": round(self.tresorerie_df["cash_out"].sum(), 2),
            "average_daily_balance": round(self.tresorerie_df["solde"].mean(), 2),
            "min_balance": round(self.tresorerie_df["solde"].min(), 2),
            "max_balance": round(self.tresorerie_df["solde"].max(), 2),
        }

    def get_daily_cash_flow(self) -> pd.DataFrame:
        """Get daily cash flow."""
        return self.tresorerie_df[["date", "cash_in", "cash_out", "solde"]].sort_values("date")

    def get_monthly_summary(self) -> pd.DataFrame:
        """Get monthly treasury summary."""
        monthly = self.tresorerie_df.copy()
        monthly["month"] = monthly["date"].dt.to_period("M")

        return (
            monthly.groupby("month")[["cash_in", "cash_out", "solde"]]
            .agg({
                "cash_in": "sum",
                "cash_out": "sum",
                "solde": "last"
            })
            .reset_index()
        )

    def get_cash_flow_trend(self) -> pd.DataFrame:
        """Get cash flow trend over time."""
        return self.get_daily_cash_flow().sort_values("date")

    def get_unreconciled_movements(self) -> pd.DataFrame:
        """Get unreconciled bank movements."""
        return self.rapprochement_df[self.rapprochement_df["statut"] == "Non rapproché"]

    def get_reconciliation_summary(self) -> Dict:
        """Get bank reconciliation summary."""
        total = len(self.rapprochement_df)
        reconciled = len(self.rapprochement_df[self.rapprochement_df["statut"] == "Rapproché"])

        return {
            "total_movements": total,
            "reconciled": reconciled,
            "unreconciled": total - reconciled,
            "reconciliation_rate_percent": round((reconciled / total * 100) if total > 0 else 0, 2),
        }

    def get_reconciliation_discrepancies(self) -> pd.DataFrame:
        """Get reconciliation discrepancies (amount differences)."""
        df = self.rapprochement_df.copy()
        df["montant_ecriture"] = pd.to_numeric(df["montant_ecriture"], errors="coerce")
        df["montant_banque"] = pd.to_numeric(df["montant_banque"], errors="coerce")
        df["difference"] = (df["montant_ecriture"] - df["montant_banque"]).abs()

        return df[df["difference"] > 0.01].sort_values("difference", ascending=False)

    def forecast_liquidity(self, days: int = 30) -> Dict:
        """Simple liquidity forecast."""
        if len(self.tresorerie_df) == 0:
            return {}

        current = self.tresorerie_df["solde"].iloc[-1]
        avg_daily_net = (self.tresorerie_df["cash_in"] - self.tresorerie_df["cash_out"]).mean()

        return {
            "current_cash": round(current, 2),
            "average_daily_net_flow": round(avg_daily_net, 2),
            f"forecast_{days}d": round(current + (avg_daily_net * days), 2),
        }

    def get_payment_dates(self) -> pd.DataFrame:
        """Get upcoming payment dates from reconciliation data."""
        df = self.rapprochement_df.copy()
        df["date_mouvement_bancaire"] = pd.to_datetime(df["date_mouvement_bancaire"], errors="coerce")
        return df.sort_values("date_mouvement_bancaire")
