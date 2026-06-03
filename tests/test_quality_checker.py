"""Unit tests for quality checker."""

import pytest
import pandas as pd
from src.quality_checker import QualityChecker


@pytest.fixture
def sample_data():
    """Create sample data."""
    return {
        "ecritures_comptables": pd.DataFrame({
            "ecriture_id": [1, 2, 3],
            "date_ecriture": ["2024-01-01", "2024-01-02", None],
            "compte_debit": ["512", "606", "999"],
            "compte_credit": ["401", "512", "401"],
            "montant": [1000, 500, 2000],
            "centre_cout": [1, None, 1],
        }),
        "factures_fournisseurs": pd.DataFrame({
            "facture_id": ["INV001", "INV002"],
            "fournisseur_id": ["SUPP001", None],
            "montant_ttc": [1000, 2000],
            "date_echeance": ["2024-01-31", None],
        }),
        "budget": pd.DataFrame({
            "budget_id": ["BDG001"],
            "budget": [10000],
            "reel": [15000],
        }),
        "tresorerie": pd.DataFrame({
            "tresorerie_id": ["TRS001"],
            "cash_in": [100000],
            "cash_out": [80000],
        }),
        "rapprochement_bancaire": pd.DataFrame({
            "rapprochement_id": ["RAPP001"],
            "montant_ecriture": [50000],
            "montant_banque": [49999],
            "statut": ["Rapproché"],
        }),
        "compte_comptable": pd.DataFrame({
            "compte_id": ["512", "606", "401"],
        }),
    }


def test_run_all_checks(sample_data):
    """Test running all checks."""
    checker = QualityChecker(sample_data)
    total_issues, score, issues = checker.run_all_checks()
    
    assert isinstance(total_issues, int)
    assert isinstance(score, float)
    assert isinstance(issues, list)
    assert 0 <= score <= 100


def test_quality_score_calculation(sample_data):
    """Test quality score calculation."""
    checker = QualityChecker(sample_data)
    total_issues, score, issues = checker.run_all_checks()
    
    # Should detect at least one issue (missing centre_cout)
    assert total_issues > 0
    assert score < 100
