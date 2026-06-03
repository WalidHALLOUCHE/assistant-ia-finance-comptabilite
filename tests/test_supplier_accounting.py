"""Unit tests for supplier accounting analyzer."""

import pytest
import pandas as pd
from src.supplier_accounting import SupplierAccountingAnalyzer


@pytest.fixture
def sample_supplier_data():
    """Create sample supplier data."""
    factures = pd.DataFrame({
        "facture_id": ["INV001", "INV002", "INV003"],
        "fournisseur_id": ["SUPP001", "SUPP002", "SUPP001"],
        "date_facture": ["2024-01-01", "2024-01-05", "2024-02-01"],
        "date_echeance": ["2024-01-31", "2024-02-05", "2024-03-01"],
        "montant_ttc": [1000, 2000, 1500],
        "montant_ht": [833, 1667, 1250],
        "statut": ["Payée", "Impayée", "Payée"],
        "date_paiement": ["2024-01-20", None, "2024-02-15"],
        "compte_charge": ["606", "615", "606"],
        "reference": ["REF001", "REF002", "REF003"],
    })
    
    fournisseurs = pd.DataFrame({
        "fournisseur_id": ["SUPP001", "SUPP002"],
        "fournisseur_nom": ["Supplier A", "Supplier B"],
        "type": ["Équipementier", "Installateur"],
        "siret": ["12345678901234", "98765432109876"],
        "adresse": ["Addr1", "Addr2"],
        "pays": ["France", "France"],
        "email": ["contact@a.com", "contact@b.com"],
    })
    
    return factures, fournisseurs


def test_summary(sample_supplier_data):
    """Test supplier summary."""
    factures, fournisseurs = sample_supplier_data
    analyzer = SupplierAccountingAnalyzer(factures, fournisseurs)
    
    summary = analyzer.get_summary()
    
    assert summary["total_invoices"] == 3
    assert summary["paid_invoices"] == 2
    assert summary["unpaid_invoices"] == 1


def test_top_suppliers(sample_supplier_data):
    """Test top suppliers."""
    factures, fournisseurs = sample_supplier_data
    analyzer = SupplierAccountingAnalyzer(factures, fournisseurs)
    
    top = analyzer.get_top_suppliers(2)
    
    assert len(top) <= 2
    assert "fournisseur_nom" in top.columns


def test_average_payment_delay(sample_supplier_data):
    """Test average payment delay."""
    factures, fournisseurs = sample_supplier_data
    analyzer = SupplierAccountingAnalyzer(factures, fournisseurs)
    
    delay = analyzer.get_average_payment_delay()
    
    assert isinstance(delay, float)
    assert delay > 0


def test_supplier_concentration(sample_supplier_data):
    """Test supplier concentration."""
    factures, fournisseurs = sample_supplier_data
    analyzer = SupplierAccountingAnalyzer(factures, fournisseurs)
    
    concentration = analyzer.get_supplier_concentration()
    
    assert "top_10_percent_of_total" in concentration
    assert concentration["active_supplier_count"] > 0
