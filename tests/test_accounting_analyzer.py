"""Unit tests for accounting analyzer."""

import pytest
import pandas as pd
from src.accounting_analyzer import AccountingAnalyzer


@pytest.fixture
def sample_data():
    """Create sample accounting data."""
    ecritures = pd.DataFrame({
        "ecriture_id": [1, 2, 3, 4],
        "date_ecriture": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
        "compte_debit": ["512", "606", "401", "701"],
        "compte_credit": ["401", "512", "512", "411"],
        "montant": [1000, 500, 2000, 1500],
        "libelle": ["Achat A", "Achat B", "Paiement", "Vente"],
        "centre_cout": [1, 1, None, 1],
        "statut": ["Validée", "Validée", "Brouillon", "Validée"],
    })
    
    comptes = pd.DataFrame({
        "compte_id": ["512", "606", "401", "701", "411"],
        "compte_libelle": ["Banque", "Achats", "Fournisseurs", "Ventes", "Clients"],
        "classe": ["Actif", "Charge", "Passif", "Produit", "Actif"],
    })
    
    return ecritures, comptes


def test_balance_sheet_summary(sample_data):
    """Test balance sheet summary."""
    ecritures, comptes = sample_data
    analyzer = AccountingAnalyzer(ecritures, comptes)
    
    summary = analyzer.get_balance_sheet_summary()
    
    assert "total_debit" in summary
    assert "total_credit" in summary
    assert "is_balanced" in summary


def test_account_balances(sample_data):
    """Test account balances."""
    ecritures, comptes = sample_data
    analyzer = AccountingAnalyzer(ecritures, comptes)
    
    balances = analyzer.get_account_balances()
    
    assert len(balances) > 0
    assert "solde" in balances.columns


def test_entries_missing_cost_center(sample_data):
    """Test detection of entries without cost center."""
    ecritures, comptes = sample_data
    analyzer = AccountingAnalyzer(ecritures, comptes)
    
    missing = analyzer.get_entries_missing_cost_center()
    
    assert len(missing) == 1  # One entry has None center


def test_entries_missing_libelle(sample_data):
    """Test detection of entries without description."""
    ecritures, comptes = sample_data
    ecritures.loc[0, "libelle"] = None
    
    analyzer = AccountingAnalyzer(ecritures, comptes)
    missing = analyzer.get_entries_missing_libelle()
    
    assert len(missing) == 1


def test_detect_anomalies(sample_data):
    """Test anomaly detection."""
    ecritures, comptes = sample_data
    analyzer = AccountingAnalyzer(ecritures, comptes)
    
    anomalies = analyzer.detect_anomalies()
    
    assert isinstance(anomalies, dict)
    assert "missing_cost_center" in anomalies
    assert anomalies["missing_cost_center"] == 1
