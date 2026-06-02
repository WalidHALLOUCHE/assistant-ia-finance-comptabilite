"""Data loading utilities."""

import os
from pathlib import Path
from typing import Optional
import pandas as pd


class DataLoader:
    """Load and cache data files."""

    def __init__(self, data_dir: Optional[str] = None):
        """Initialize data loader."""
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / "data"
        self.data_dir = Path(data_dir)

    def load_ecritures_comptables(self) -> pd.DataFrame:
        """Load accounting entries."""
        return self._load_csv("fact_ecritures_comptables.csv")

    def load_budget(self) -> pd.DataFrame:
        """Load budget data."""
        return self._load_csv("fact_budget.csv")

    def load_factures_fournisseurs(self) -> pd.DataFrame:
        """Load supplier invoices."""
        return self._load_csv("fact_factures_fournisseurs.csv")

    def load_tresorerie(self) -> pd.DataFrame:
        """Load treasury data."""
        return self._load_csv("fact_tresorerie.csv")

    def load_rapprochement_bancaire(self) -> pd.DataFrame:
        """Load bank reconciliation data."""
        return self._load_csv("fact_rapprochement_bancaire.csv")

    def load_compte_comptable(self) -> pd.DataFrame:
        """Load accounting accounts dimension."""
        return self._load_csv("dim_compte_comptable.csv")

    def load_centre_cout(self) -> pd.DataFrame:
        """Load cost center dimension."""
        return self._load_csv("dim_centre_cout.csv")

    def load_projet(self) -> pd.DataFrame:
        """Load project dimension."""
        return self._load_csv("dim_projet.csv")

    def load_fournisseur(self) -> pd.DataFrame:
        """Load supplier dimension."""
        return self._load_csv("dim_fournisseur.csv")

    def load_date(self) -> pd.DataFrame:
        """Load date dimension."""
        return self._load_csv("dim_date.csv")

    def _load_csv(self, filename: str) -> pd.DataFrame:
        """Load a CSV file from the data directory."""
        filepath = self.data_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Data file not found: {filepath}")
        return pd.read_csv(filepath)

    def load_all_data(self) -> dict[str, pd.DataFrame]:
        """Load all data files."""
        return {
            "ecritures_comptables": self.load_ecritures_comptables(),
            "budget": self.load_budget(),
            "factures_fournisseurs": self.load_factures_fournisseurs(),
            "tresorerie": self.load_tresorerie(),
            "rapprochement_bancaire": self.load_rapprochement_bancaire(),
            "compte_comptable": self.load_compte_comptable(),
            "centre_cout": self.load_centre_cout(),
            "projet": self.load_projet(),
            "fournisseur": self.load_fournisseur(),
            "date": self.load_date(),
        }
