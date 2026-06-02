"""Data quality checks and monitoring."""

import pandas as pd
from typing import Dict, List, Tuple


class QualityChecker:
    """Check data quality across all datasets."""

    def __init__(self, data_dict: Dict[str, pd.DataFrame]):
        """Initialize checker with all datasets."""
        self.data = data_dict
        self.issues = []

    def run_all_checks(self) -> Tuple[int, float, List[Dict]]:
        """Run all quality checks."""
        self.issues = []

        self.check_accounting_entries()
        self.check_supplier_invoices()
        self.check_budget_data()
        self.check_treasury_data()
        self.check_reconciliation()

        return self._get_quality_score()

    def check_accounting_entries(self):
        """Check accounting entries quality."""
        df = self.data.get("ecritures_comptables")
        if df is None:
            return

        # Missing required fields
        for col in ["date_ecriture", "compte_debit", "compte_credit", "montant"]:
            missing = df[df[col].isna()].shape[0]
            if missing > 0:
                self.issues.append({
                    "category": "Comptabilité",
                    "type": f"Champ manquant: {col}",
                    "count": missing,
                    "severity": "high",
                })

        # Missing cost center
        missing_cc = df[df["centre_cout"].isna()].shape[0]
        if missing_cc > 0:
            self.issues.append({
                "category": "Comptabilité",
                "type": "Écritures sans centre de coût",
                "count": missing_cc,
                "severity": "medium",
            })

        # Invalid accounts
        valid_accounts = set(self.data.get("compte_comptable", pd.DataFrame())["compte_id"].values)
        if len(valid_accounts) > 0:
            invalid_debit = df[~df["compte_debit"].isin(valid_accounts)].shape[0]
            invalid_credit = df[~df["compte_credit"].isin(valid_accounts)].shape[0]
            if invalid_debit + invalid_credit > 0:
                self.issues.append({
                    "category": "Comptabilité",
                    "type": "Comptes comptables invalides",
                    "count": invalid_debit + invalid_credit,
                    "severity": "high",
                })

    def check_supplier_invoices(self):
        """Check supplier invoices quality."""
        df = self.data.get("factures_fournisseurs")
        if df is None:
            return

        # Missing due date
        missing_due = df[df["date_echeance"].isna()].shape[0]
        if missing_due > 0:
            self.issues.append({
                "category": "Fournisseurs",
                "type": "Factures sans date d'échéance",
                "count": missing_due,
                "severity": "high",
            })

        # Missing supplier
        missing_supp = df[df["fournisseur_id"].isna()].shape[0]
        if missing_supp > 0:
            self.issues.append({
                "category": "Fournisseurs",
                "type": "Factures sans fournisseur",
                "count": missing_supp,
                "severity": "high",
            })

        # Negative amounts
        negative = df[df["montant_ttc"] < 0].shape[0]
        if negative > 0:
            self.issues.append({
                "category": "Fournisseurs",
                "type": "Montants négatifs",
                "count": negative,
                "severity": "medium",
            })

    def check_budget_data(self):
        """Check budget data quality."""
        df = self.data.get("budget")
        if df is None:
            return

        # Negative amounts
        negative = df[(df["budget"] < 0) | (df["reel"] < 0)].shape[0]
        if negative > 0:
            self.issues.append({
                "category": "Budget",
                "type": "Montants budgétaires négatifs",
                "count": negative,
                "severity": "medium",
            })

        # Large variances
        df_copy = df.copy()
        if "ecart" not in df_copy.columns:
            df_copy["ecart"] = pd.to_numeric(df_copy["reel"], errors="coerce") - pd.to_numeric(
                df_copy["budget"], errors="coerce"
            )
        df_copy["variance_pct"] = (df_copy["ecart"] / df_copy["budget"] * 100).abs()
        large_var = df_copy[df_copy["variance_pct"] > 50].shape[0]
        if large_var > 0:
            self.issues.append({
                "category": "Budget",
                "type": "Écarts budgétaires > 50%",
                "count": large_var,
                "severity": "medium",
            })

    def check_treasury_data(self):
        """Check treasury data quality."""
        df = self.data.get("tresorerie")
        if df is None:
            return

        # Missing values
        for col in ["cash_in", "cash_out", "solde"]:
            if col not in df.columns:
                continue
            missing = df[df[col].isna()].shape[0]
            if missing > 0:
                self.issues.append({
                    "category": "Trésorerie",
                    "type": f"Valeurs manquantes: {col}",
                    "count": missing,
                    "severity": "high",
                })

    def check_reconciliation(self):
        """Check reconciliation data quality."""
        df = self.data.get("rapprochement_bancaire")
        if df is None:
            return

        # Unreconciled items
        unreconciled = df[df["statut"] == "Non rapproché"].shape[0]
        if unreconciled > 0:
            self.issues.append({
                "category": "Rapprochement",
                "type": "Mouvements non rapprochés",
                "count": unreconciled,
                "severity": "medium",
            })

        # Amount discrepancies
        df_copy = df.copy()
        df_copy["montant_ecriture"] = pd.to_numeric(df_copy["montant_ecriture"], errors="coerce")
        df_copy["montant_banque"] = pd.to_numeric(df_copy["montant_banque"], errors="coerce")
        discrepancies = df_copy[(df_copy["montant_ecriture"] - df_copy["montant_banque"]).abs() > 0.01].shape[0]
        if discrepancies > 0:
            self.issues.append({
                "category": "Rapprochement",
                "type": "Écarts de montant",
                "count": discrepancies,
                "severity": "high",
            })

    def _get_quality_score(self) -> Tuple[int, float, List[Dict]]:
        """Calculate quality score."""
        total_issues = sum(issue["count"] for issue in self.issues)
        total_records = sum(len(df) for df in self.data.values())

        quality_score = max(0, 100 - (total_issues / total_records * 100)) if total_records > 0 else 100

        return total_issues, round(quality_score, 2), self.issues

    def get_issue_summary(self) -> pd.DataFrame:
        """Get summary of issues."""
        if not self.issues:
            return pd.DataFrame(columns=["Catégorie", "Type", "Nombre", "Sévérité"])

        summary = pd.DataFrame(self.issues)
        return summary.groupby("category").agg({
            "count": "sum",
            "type": "count",
        }).reset_index().rename(columns={
            "count": "total_issues",
            "type": "issue_types"
        })

    def get_recommendations(self) -> List[str]:
        """Get recommendations based on issues."""
        recommendations = []

        high_severity = [i for i in self.issues if i["severity"] == "high"]
        if high_severity:
            recommendations.append(
                f"🔴 {len(high_severity)} problèmes critiques détectés - Action immédiate requise"
            )

        low_quality = sum(i["count"] for i in self.issues) > 50
        if low_quality:
            recommendations.append("⚠️  Qualité des données insuffisante - Audit recommandé")

        return recommendations
