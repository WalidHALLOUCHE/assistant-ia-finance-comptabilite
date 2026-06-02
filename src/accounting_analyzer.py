"""Accounting analysis and validation."""

import pandas as pd
from typing import Tuple, List, Dict


class AccountingAnalyzer:
    """Analyze general accounting data."""

    def __init__(self, ecritures_df: pd.DataFrame, comptes_df: pd.DataFrame):
        """Initialize analyzer."""
        self.ecritures_df = ecritures_df.copy()
        self.comptes_df = comptes_df.copy()
        self._prepare_data()

    def _prepare_data(self):
        """Prepare data for analysis."""
        self.ecritures_df["montant"] = pd.to_numeric(
            self.ecritures_df["montant"], errors="coerce"
        )
        self.ecritures_df["date_ecriture"] = pd.to_datetime(
            self.ecritures_df["date_ecriture"], errors="coerce"
        )

    def get_balance_sheet_summary(self) -> Dict:
        """Get balance sheet summary."""
        total_debit = self.ecritures_df["montant"].sum()
        total_credit = self.ecritures_df["montant"].sum()

        return {
            "total_debit": total_debit,
            "total_credit": total_credit,
            "difference": abs(total_debit - total_credit),
            "is_balanced": abs(total_debit - total_credit) < 0.01,
        }

    def get_account_balances(self) -> pd.DataFrame:
        """Get balance by account."""
        debit = (
            self.ecritures_df.groupby("compte_debit")["montant"]
            .sum()
            .reset_index()
        )
        debit.columns = ["compte", "debit"]

        credit = (
            self.ecritures_df.groupby("compte_credit")["montant"]
            .sum()
            .reset_index()
        )
        credit.columns = ["compte", "credit"]

        balances = pd.merge(debit, credit, on="compte", how="outer").fillna(0)
        balances["solde"] = balances["debit"] - balances["credit"]

        return balances.sort_values("solde", ascending=False)

    def get_account_class_balances(self) -> pd.DataFrame:
        """Get balance by account class."""
        balances = self.get_account_balances()
        balances = balances.merge(
            self.comptes_df[["compte_id", "classe"]], left_on="compte", right_on="compte_id", how="left"
        )

        return (
            balances.groupby("classe")[["debit", "credit", "solde"]]
            .sum()
            .reset_index()
        )

    def get_unbalanced_entries(self) -> pd.DataFrame:
        """Get entries that are not balanced (same piece/journal)."""
        if "numero_piece" not in self.ecritures_df.columns:
            return pd.DataFrame(columns=self.ecritures_df.columns)

        grouped = self.ecritures_df.groupby("numero_piece")["montant"].sum()

        unbalanced = grouped[grouped != 0].reset_index()
        return self.ecritures_df[
            self.ecritures_df["numero_piece"].isin(unbalanced["numero_piece"])
        ]

    def get_entries_missing_libelle(self) -> pd.DataFrame:
        """Get entries without description."""
        return self.ecritures_df[
            self.ecritures_df["libelle"].isna()
            | (self.ecritures_df["libelle"] == "")
        ]

    def get_entries_missing_cost_center(self) -> pd.DataFrame:
        """Get entries without cost center assignment."""
        return self.ecritures_df[
            self.ecritures_df["centre_cout"].isna()
            | (self.ecritures_df["centre_cout"] == "")
        ]

    def get_entries_invalid_accounts(self) -> pd.DataFrame:
        """Get entries with invalid account codes."""
        valid_accounts = set(self.comptes_df["compte_id"].values)

        invalid_entries = self.ecritures_df[
            (~self.ecritures_df["compte_debit"].isin(valid_accounts))
            | (~self.ecritures_df["compte_credit"].isin(valid_accounts))
        ]
        return invalid_entries

    def get_entries_with_status(self, status: str) -> pd.DataFrame:
        """Get entries with specific status."""
        return self.ecritures_df[self.ecritures_df["statut"] == status]

    def get_monthly_summary(self) -> pd.DataFrame:
        """Get monthly accounting summary."""
        monthly = self.ecritures_df.copy()
        monthly["month"] = monthly["date_ecriture"].dt.to_period("M").astype(str)

        summary = monthly.groupby("month").agg(
            total_amount=("montant", "sum"),
            entry_count=("montant", "count"),
        ).reset_index()

        return summary

    def get_journal_summary(self) -> pd.DataFrame:
        """Get summary by journal."""
        return self.ecritures_df.groupby("journal").agg(
            total_amount=("montant", "sum"),
            entry_count=("montant", "count"),
        ).reset_index()

    def detect_anomalies(self) -> Dict[str, List]:
        """Detect accounting anomalies."""
        anomalies = {
            "unbalanced_entries": len(self.get_unbalanced_entries()),
            "missing_libelle": len(self.get_entries_missing_libelle()),
            "missing_cost_center": len(self.get_entries_missing_cost_center()),
            "invalid_accounts": len(self.get_entries_invalid_accounts()),
            "draft_entries": len(self.get_entries_with_status("Brouillon")),
        }
        return anomalies
