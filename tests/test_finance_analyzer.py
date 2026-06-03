"""Unit tests for finance analyzer."""

import pytest
import pandas as pd
from src.finance_analyzer import FinanceAnalyzer


@pytest.fixture
def sample_budget_data():
    """Create sample budget data."""
    budget = pd.DataFrame({
        "budget_id": ["BDG001", "BDG002", "BDG003"],
        "mois": [1, 1, 2],
        "centre_cout": [1, 2, 1],
        "compte": ["606", "615", "606"],
        "budget": [10000, 5000, 12000],
        "reel": [9500, 5500, 13000],
        "ecart": [-500, 500, 1000],
    })
    
    ecritures = pd.DataFrame({
        "ecriture_id": [1, 2, 3],
        "date_ecriture": ["2024-01-01", "2024-01-02", "2024-02-01"],
        "compte_debit": ["606", "615", "606"],
        "compte_credit": ["401", "401", "401"],
        "montant": [9500, 5500, 13000],
    })
    
    return budget, ecritures


def test_budget_summary(sample_budget_data):
    """Test budget summary."""
    budget, ecritures = sample_budget_data
    analyzer = FinanceAnalyzer(budget, ecritures)
    
    summary = analyzer.get_budget_summary()
    
    assert "total_budget" in summary
    assert "total_real" in summary
    assert "total_variance" in summary
    assert summary["total_budget"] == 27000


def test_cost_center_analysis(sample_budget_data):
    """Test cost center analysis."""
    budget, ecritures = sample_budget_data
    analyzer = FinanceAnalyzer(budget, ecritures)
    
    analysis = analyzer.get_cost_center_analysis()
    
    assert len(analysis) == 2
    assert "variance_percent" in analysis.columns


def test_top_variances(sample_budget_data):
    """Test top variances."""
    budget, ecritures = sample_budget_data
    analyzer = FinanceAnalyzer(budget, ecritures)
    
    variances = analyzer.get_top_variances(2, "negative")
    
    assert len(variances) <= 2


def test_budget_consumption_rate(sample_budget_data):
    """Test budget consumption rate."""
    budget, ecritures = sample_budget_data
    analyzer = FinanceAnalyzer(budget, ecritures)
    
    rate = analyzer.get_budget_consumption_rate()
    
    assert isinstance(rate, float)
    assert 0 <= rate <= 200


def test_is_on_track(sample_budget_data):
    """Test if budget is on track."""
    budget, ecritures = sample_budget_data
    analyzer = FinanceAnalyzer(budget, ecritures)
    
    on_track = analyzer.is_on_track(tolerance_percent=10)
    
    assert isinstance(on_track, bool)
