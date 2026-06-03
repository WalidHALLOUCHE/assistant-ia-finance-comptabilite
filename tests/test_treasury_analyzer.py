"""Unit tests for treasury analyzer."""

import pytest
import pandas as pd
from src.treasury_analyzer import TreasuryAnalyzer


@pytest.fixture
def sample_treasury_data():
    """Create sample treasury data."""
    tresorerie = pd.DataFrame({
        "tresorerie_id": ["TRS001", "TRS002", "TRS003"],
        "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "cash_in": [100000, 150000, 120000],
        "cash_out": [80000, 90000, 110000],
        "solde": [200000, 260000, 270000],
    })
    
    rapprochement = pd.DataFrame({
        "rapprochement_id": ["RAPP001", "RAPP002"],
        "date_ecriture": ["2024-01-01", "2024-01-02"],
        "date_mouvement_bancaire": ["2024-01-01", "2024-01-02"],
        "montant_ecriture": [50000, 75000],
        "montant_banque": [50000, 75000],
        "statut": ["Rapproché", "Rapproché"],
        "description": ["Paiement A", "Paiement B"],
    })
    
    return tresorerie, rapprochement


def test_treasury_summary(sample_treasury_data):
    """Test treasury summary."""
    tresorerie, rapprochement = sample_treasury_data
    analyzer = TreasuryAnalyzer(tresorerie, rapprochement)
    
    summary = analyzer.get_treasury_summary()
    
    assert "current_cash" in summary
    assert "total_cash_in" in summary
    assert "total_cash_out" in summary
    assert summary["current_cash"] == 270000


def test_monthly_summary(sample_treasury_data):
    """Test monthly summary."""
    tresorerie, rapprochement = sample_treasury_data
    analyzer = TreasuryAnalyzer(tresorerie, rapprochement)
    
    monthly = analyzer.get_monthly_summary()
    
    assert len(monthly) > 0
    assert "cash_in" in monthly.columns


def test_reconciliation_summary(sample_treasury_data):
    """Test reconciliation summary."""
    tresorerie, rapprochement = sample_treasury_data
    analyzer = TreasuryAnalyzer(tresorerie, rapprochement)
    
    recon = analyzer.get_reconciliation_summary()
    
    assert recon["total_movements"] == 2
    assert recon["reconciliation_rate_percent"] == 100


def test_forecast_liquidity(sample_treasury_data):
    """Test liquidity forecast."""
    tresorerie, rapprochement = sample_treasury_data
    analyzer = TreasuryAnalyzer(tresorerie, rapprochement)
    
    forecast = analyzer.forecast_liquidity(30)
    
    assert "current_cash" in forecast
    assert "forecast_30d" in forecast
