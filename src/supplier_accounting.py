"""Supplier accounting and payables analysis."""

import pandas as pd
from datetime import datetime
from typing import Dict, List


class SupplierAccountingAnalyzer:
    """Analyze supplier invoices and accounts payable."""

    def __init__(self, factures_df: pd.DataFrame, fournisseurs_df: pd.DataFrame):
        """Initialize analyzer."""
        self.factures_df = factures_df.copy()
        self.fournisseurs_df = fournisseurs_df.copy()
        self._prepare_data()

    def _prepare_data(self):
        """Prepare data for analysis."""
        self.factures_df["montant_ttc"] = pd.to_numeric(
            self.factures_df["montant_ttc"], errors="coerce"
        )
        self.factures_df["montant_ht"] = pd.to_numeric(
            self.factures_df["montant_ht"], errors="coerce"
        )
        self.factures_df["date_facture"] = pd.to_datetime(
            self.factures_df["date_facture"], errors="coerce"
        )
        self.factures_df["date_echeance"] = pd.to_datetime(
            self.factures_df["date_echeance"], errors="coerce"
        )
        if "date_paiement" in self.factures_df.columns:
            paiement = self.factures_df["date_paiement"].replace({"None": None, "": None})
            self.factures_df["date_paiement"] = pd.to_datetime(paiement, errors="coerce")
        else:
            self.factures_df["date_paiement"] = pd.NaT

    def get_summary(self) -> Dict:
        """Get accounts payable summary."""
        return {
            "total_invoices": len(self.factures_df),
            "total_amount": round(self.factures_df["montant_ttc"].sum(), 2),
            "paid_invoices": len(self.factures_df[self.factures_df["statut"] == "Payée"]),
            "unpaid_invoices": len(self.factures_df[self.factures_df["statut"] != "Payée"]),
            "overdue_invoices": len(self.get_overdue_invoices()),
            "overdue_amount": round(self.get_overdue_invoices()["montant_ttc"].sum(), 2),
        }

    def get_top_suppliers(self, top_n: int = 10) -> pd.DataFrame:
        """Get top suppliers by total amount."""
        top = (
            self.factures_df.groupby("fournisseur_id")[["montant_ttc"]]
            .sum()
            .reset_index()
            .sort_values("montant_ttc", ascending=False)
            .head(top_n)
        )

        top = top.merge(
            self.fournisseurs_df[["fournisseur_id", "fournisseur_nom"]],
            on="fournisseur_id",
            how="left"
        )

        return top.rename(columns={"montant_ttc": "total_amount"})

    def get_overdue_invoices(self) -> pd.DataFrame:
        """Get all overdue invoices."""
        today = datetime.now().date()
        overdue = self.factures_df[
            (self.factures_df["date_echeance"].dt.date < today)
            & (self.factures_df["statut"] != "Payée")
        ]
        return overdue

    def get_invoices_by_status(self) -> pd.DataFrame:
        """Get invoice count and amount by status."""
        return (
            self.factures_df.groupby("statut")
            .agg(
                {
                    "facture_id": "count",
                    "montant_ttc": "sum",
                }
            )
            .reset_index()
            .rename(columns={
                "facture_id": "count",
                "montant_ttc": "amount"
            })
        )

    def get_average_payment_delay(self) -> float:
        """Get average payment delay in days."""
        paid = self.factures_df[
            (self.factures_df["statut"] == "Payée")
            & (self.factures_df["date_paiement"].notna())
        ].copy()

        if len(paid) == 0:
            return 0.0

        paid["delay"] = (paid["date_paiement"] - paid["date_facture"]).dt.days
        return float(paid["delay"].mean())

    def get_payment_performance_by_supplier(self) -> pd.DataFrame:
        """Analyze payment performance by supplier."""
        paid = self.factures_df[self.factures_df["statut"] == "Payée"].copy()

        if len(paid) == 0:
            return pd.DataFrame()

        paid["delay"] = (paid["date_paiement"] - paid["date_facture"]).dt.days

        performance = (
            paid.groupby("fournisseur_id")
            .agg(
                {
                    "facture_id": "count",
                    "delay": "mean",
                    "montant_ttc": "sum",
                }
            )
            .reset_index()
            .rename(columns={
                "facture_id": "invoice_count",
                "delay": "avg_payment_days",
                "montant_ttc": "total_amount"
            })
        )

        performance = performance.merge(
            self.fournisseurs_df[["fournisseur_id", "fournisseur_nom"]],
            on="fournisseur_id",
            how="left"
        )

        return performance.sort_values("avg_payment_days", ascending=False)

    def get_invoices_missing_supplier(self) -> pd.DataFrame:
        """Get invoices without supplier."""
        return self.factures_df[
            self.factures_df["fournisseur_id"].isna()
            | (self.factures_df["fournisseur_id"] == "")
        ]

    def get_invoices_missing_due_date(self) -> pd.DataFrame:
        """Get invoices without due date."""
        return self.factures_df[
            self.factures_df["date_echeance"].isna()
            | (self.factures_df["date_echeance"] == "")
        ]

    def get_monthly_supplier_expenses(self) -> pd.DataFrame:
        """Get supplier expenses by month."""
        monthly = self.factures_df.copy()
        monthly["month"] = monthly["date_facture"].dt.to_period("M")

        return (
            monthly.groupby("month")[["montant_ttc"]]
            .sum()
            .reset_index()
            .rename(columns={"montant_ttc": "total_expenses"})
        )

    def get_supplier_concentration(self) -> Dict:
        """Analyze supplier concentration."""
        total = self.factures_df["montant_ttc"].sum()
        top_10 = self.get_top_suppliers(10)["total_amount"].sum()

        return {
            "top_10_percent_of_total": round((top_10 / total * 100) if total > 0 else 0, 2),
            "supplier_count": len(self.fournisseurs_df),
            "active_supplier_count": self.factures_df["fournisseur_id"].nunique(),
        }
