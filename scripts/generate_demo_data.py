"""Generate realistic fictional financial data for a generic business."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Define company parameters
MONTHS = 12
START_DATE = datetime(2024, 1, 1)
NUM_PROJECTS = 20
NUM_SUPPLIERS = 35
NUM_COST_CENTERS = 10
NUM_ACCOUNTING_ENTRIES = 600


def generate_date_dimension():
    """Generate date dimension table."""
    dates = []
    for i in range(365):
        date = START_DATE + timedelta(days=i)
        dates.append({
            "date_id": date.strftime("%Y%m%d"),
            "date": date.strftime("%Y-%m-%d"),
            "year": date.year,
            "month": date.month,
            "month_name": date.strftime("%B"),
            "day": date.day,
            "week": date.isocalendar()[1],
            "quarter": (date.month - 1) // 3 + 1,
        })
    return pd.DataFrame(dates)


def generate_cost_centers():
    """Generate cost center dimension."""
    cost_centers = [
        "Finance",
        "Comptabilité",
        "Contrôle de Gestion",
        "IT",
        "RH",
        "Juridique",
        "Achats",
        "Maintenance",
        "Construction",
        "Exploitation",
    ]
    
    df = pd.DataFrame({
        "centre_cout_id": range(1, len(cost_centers) + 1),
        "centre_cout": cost_centers,
        "responsable": [f"Resp_{cc.replace(' ', '_')}" for cc in cost_centers],
    })
    return df


def generate_accounting_accounts():
    """Generate accounting accounts dimension."""
    accounts = [
        ("401", "Fournisseurs", "Passif"),
        ("411", "Clients", "Actif"),
        ("512", "Banque", "Actif"),
        ("606", "Achats non stockés", "Charge"),
        ("615", "Maintenance", "Charge"),
        ("622", "Honoraires", "Charge"),
        ("623", "Publicité", "Charge"),
        ("625", "Déplacements", "Charge"),
        ("626", "Frais postaux et télécoms", "Charge"),
        ("641", "Salaires", "Charge"),
        ("681", "Dotations aux amortissements", "Charge"),
        ("701", "Ventes énergie", "Produit"),
        ("706", "Prestations de services", "Produit"),
    ]
    
    df = pd.DataFrame(accounts, columns=["compte_id", "compte_libelle", "classe"])
    return df


def generate_projects():
    """Generate projects dimension."""
    regions = ["Nord", "Sud-Est", "Ouest", "Centre", "Est"]
    projects = []
    
    for i in range(NUM_PROJECTS):
        projects.append({
            "projet_id": f"PROJ_{i+1:03d}",
            "projet_nom": f"Projet {regions[i % len(regions)]} - Phase {(i // 5) + 1}",
            "region": regions[i % len(regions)],
            "capacite_mwc": round(np.random.uniform(0.5, 10), 2),
            "date_debut": (START_DATE + timedelta(days=np.random.randint(0, 300))).strftime("%Y-%m-%d"),
            "statut": np.random.choice(["En cours", "Terminé", "Planifié"], p=[0.5, 0.3, 0.2]),
            "budget_total": round(np.random.uniform(100000, 2000000), 2),
        })
    
    return pd.DataFrame(projects)


def generate_suppliers():
    """Generate suppliers dimension."""
    supplier_types = ["Équipementier", "Installateur", "Sous-traitant", "Consulting"]
    
    suppliers = []
    for i in range(NUM_SUPPLIERS):
        suppliers.append({
            "fournisseur_id": f"SUPP_{i+1:03d}",
            "fournisseur_nom": f"Fournisseur {i+1} - {supplier_types[i % len(supplier_types)]}",
            "type": supplier_types[i % len(supplier_types)],
            "siret": f"{9072449999900 + i}",
            "adresse": f"{i+1} rue Principale, 75000 Paris",
            "pays": "France",
            "email": f"contact{i+1}@supplier.com",
        })
    
    return pd.DataFrame(suppliers)


def generate_accounting_entries():
    """Generate accounting entries."""
    accounts_df = generate_accounting_accounts()
    cost_centers_df = generate_cost_centers()
    projects_df = generate_projects()
    
    entries = []
    entry_id = 1
    
    for month in range(1, MONTHS + 1):
        month_start = START_DATE.replace(month=month)
        
        # Operating expenses
        for _ in range(40):
            entry_date = month_start + timedelta(days=np.random.randint(0, 28))
            amount = round(np.random.uniform(500, 50000), 2)
            
            entries.append({
                "ecriture_id": entry_id,
                "date_ecriture": entry_date.strftime("%Y-%m-%d"),
                "journal": np.random.choice(["AC", "VE", "OP", "TR"]),
                "numero_piece": f"PJ_{entry_id:06d}",
                "compte_debit": np.random.choice(accounts_df[accounts_df["classe"] == "Charge"]["compte_id"].values),
                "compte_credit": "401",
                "montant": amount,
                "libelle": np.random.choice([
                    "Facture fournisseur",
                    "Achats matériaux",
                    "Services sous-traitance",
                    "Maintenance",
                    "Honoraires consultant",
                ]),
                "centre_cout": np.random.choice(cost_centers_df["centre_cout_id"].values),
                "projet": np.random.choice(projects_df["projet_id"].values) if np.random.rand() > 0.3 else None,
                "statut": np.random.choice(["Validée", "Brouillon", "Pointée"], p=[0.85, 0.1, 0.05]),
            })
            entry_id += 1
        
        # Revenue entries
        for _ in range(15):
            entry_date = month_start + timedelta(days=np.random.randint(0, 28))
            amount = round(np.random.uniform(10000, 150000), 2)
            
            entries.append({
                "ecriture_id": entry_id,
                "date_ecriture": entry_date.strftime("%Y-%m-%d"),
                "journal": "VE",
                "numero_piece": f"FA_{entry_id:06d}",
                "compte_debit": "411",
                "compte_credit": np.random.choice(["701", "706"]),
                "montant": amount,
                "libelle": "Facture client",
                "centre_cout": np.random.choice(cost_centers_df["centre_cout_id"].values),
                "projet": np.random.choice(projects_df["projet_id"].values),
                "statut": np.random.choice(["Validée", "Brouillon"], p=[0.95, 0.05]),
            })
            entry_id += 1
        
        # Bank transactions
        for _ in range(8):
            entry_date = month_start + timedelta(days=np.random.randint(0, 28))
            
            if np.random.rand() > 0.4:  # Payment
                amount = round(np.random.uniform(5000, 100000), 2)
                entries.append({
                    "ecriture_id": entry_id,
                    "date_ecriture": entry_date.strftime("%Y-%m-%d"),
                    "journal": "TR",
                    "numero_piece": f"BQ_{entry_id:06d}",
                    "compte_debit": "401",
                    "compte_credit": "512",
                    "montant": amount,
                    "libelle": "Paiement fournisseur",
                    "centre_cout": np.random.choice(cost_centers_df["centre_cout_id"].values),
                    "projet": None,
                    "statut": "Validée",
                })
            else:  # Receipt
                amount = round(np.random.uniform(10000, 200000), 2)
                entries.append({
                    "ecriture_id": entry_id,
                    "date_ecriture": entry_date.strftime("%Y-%m-%d"),
                    "journal": "TR",
                    "numero_piece": f"BQ_{entry_id:06d}",
                    "compte_debit": "512",
                    "compte_credit": "411",
                    "montant": amount,
                    "libelle": "Encaissement client",
                    "centre_cout": np.random.choice(cost_centers_df["centre_cout_id"].values),
                    "projet": np.random.choice(projects_df["projet_id"].values),
                    "statut": "Validée",
                })
            
            entry_id += 1
    
    return pd.DataFrame(entries)


def generate_supplier_invoices():
    """Generate supplier invoices."""
    suppliers_df = generate_suppliers()
    accounts_df = generate_accounting_accounts()
    
    invoices = []
    invoice_id = 1
    
    for month in range(1, MONTHS + 1):
        month_start = START_DATE.replace(month=month)
        
        for _ in range(10):
            invoice_date = month_start + timedelta(days=np.random.randint(0, 28))
            due_date = invoice_date + timedelta(days=int(np.random.choice([15, 30, 45, 60])))
            amount = round(np.random.uniform(1000, 100000), 2)
            
            is_overdue = due_date < datetime.now()
            is_paid = np.random.choice([True, False], p=[0.6, 0.4])
            
            invoices.append({
                "facture_id": f"INV_{invoice_id:06d}",
                "fournisseur_id": np.random.choice(suppliers_df["fournisseur_id"].values),
                "date_facture": invoice_date.strftime("%Y-%m-%d"),
                "date_echeance": due_date.strftime("%Y-%m-%d"),
                "montant_ht": amount,
                "tva_montant": round(amount * 0.20, 2),
                "montant_ttc": round(amount * 1.20, 2),
                "statut": "Payée" if is_paid else ("Echue" if is_overdue else "Impayée"),
                "date_paiement": (invoice_date + timedelta(days=np.random.randint(5, 60))).strftime("%Y-%m-%d") if is_paid else None,
                "compte_charge": np.random.choice(accounts_df[accounts_df["classe"] == "Charge"]["compte_id"].values),
                "reference": f"REF_{invoice_id}",
            })
            invoice_id += 1
    
    return pd.DataFrame(invoices)


def generate_budget():
    """Generate budget data."""
    accounts_df = generate_accounting_accounts()
    cost_centers_df = generate_cost_centers()
    projects_df = generate_projects()
    
    budget_data = []
    
    for month in range(1, MONTHS + 1):
        for cost_center in cost_centers_df["centre_cout_id"].values[:5]:  # Limit to 5 cost centers
            for account in accounts_df[accounts_df["classe"] == "Charge"]["compte_id"].values:
                budget_amount = round(np.random.uniform(5000, 100000), 2)
                real_amount = round(budget_amount * np.random.uniform(0.8, 1.2), 2)
                
                budget_data.append({
                    "budget_id": f"BDG_{len(budget_data)+1:06d}",
                    "mois": month,
                    "centre_cout": cost_center,
                    "compte": account,
                    "budget": budget_amount,
                    "reel": real_amount,
                    "ecart": round(real_amount - budget_amount, 2),
                })
    
    return pd.DataFrame(budget_data)


def generate_treasury():
    """Generate treasury data."""
    entries = []
    
    for month in range(1, MONTHS + 1):
        month_start = START_DATE.replace(month=month)
        
        for day in range(1, 29):
            try:
                date = month_start.replace(day=day)
            except ValueError:
                break
            
            cash_in = round(np.random.uniform(50000, 500000), 2)
            cash_out = round(np.random.uniform(30000, 300000), 2)
            
            entries.append({
                "tresorerie_id": f"TRS_{len(entries)+1:06d}",
                "date": date.strftime("%Y-%m-%d"),
                "cash_in": cash_in,
                "cash_out": cash_out,
                "solde": round(1000000 - (cash_out - cash_in) + np.random.uniform(-50000, 50000), 2),
            })
    
    return pd.DataFrame(entries)


def generate_bank_reconciliation():
    """Generate bank reconciliation data."""
    entries = []
    
    invoices_df = generate_supplier_invoices()
    
    for idx, row in invoices_df.iterrows():
        if row["statut"] == "Payée":
            entries.append({
                "rapprochement_id": f"RAPP_{idx+1:06d}",
                "date_ecriture": row["date_paiement"],
                "date_mouvement_bancaire": (datetime.strptime(row["date_paiement"], "%Y-%m-%d") + timedelta(days=np.random.randint(0, 2))).strftime("%Y-%m-%d"),
                "montant_ecriture": row["montant_ttc"],
                "montant_banque": row["montant_ttc"],
                "statut": "Rapproché" if np.random.rand() > 0.05 else "Non rapproché",
                "description": f"Paiement {row['facture_id']}",
            })
    
    return pd.DataFrame(entries)


def main():
    """Generate all data files."""
    print("🔄 Generating financial data...")
    
    print("  📅 Generating date dimension...")
    dates_df = generate_date_dimension()
    dates_df.to_csv(DATA_DIR / "dim_date.csv", index=False)
    
    print("  📊 Generating cost centers...")
    cost_centers_df = generate_cost_centers()
    cost_centers_df.to_csv(DATA_DIR / "dim_centre_cout.csv", index=False)
    
    print("  💰 Generating accounting accounts...")
    accounts_df = generate_accounting_accounts()
    accounts_df.to_csv(DATA_DIR / "dim_compte_comptable.csv", index=False)
    
    print("  📊 Generating projects...")
    projects_df = generate_projects()
    projects_df.to_csv(DATA_DIR / "dim_projet.csv", index=False)
    
    print("  🏢 Generating suppliers...")
    suppliers_df = generate_suppliers()
    suppliers_df.to_csv(DATA_DIR / "dim_fournisseur.csv", index=False)
    
    print("  ✍️ Generating accounting entries...")
    entries_df = generate_accounting_entries()
    entries_df.to_csv(DATA_DIR / "fact_ecritures_comptables.csv", index=False)
    
    print("  📄 Generating supplier invoices...")
    invoices_df = generate_supplier_invoices()
    invoices_df.to_csv(DATA_DIR / "fact_factures_fournisseurs.csv", index=False)
    
    print("  📈 Generating budget data...")
    budget_df = generate_budget()
    budget_df.to_csv(DATA_DIR / "fact_budget.csv", index=False)
    
    print("  💳 Generating treasury data...")
    treasury_df = generate_treasury()
    treasury_df.to_csv(DATA_DIR / "fact_tresorerie.csv", index=False)
    
    print("  🔄 Generating bank reconciliation...")
    reconciliation_df = generate_bank_reconciliation()
    reconciliation_df.to_csv(DATA_DIR / "fact_rapprochement_bancaire.csv", index=False)
    
    print("\n✅ Data generation complete!")
    print(f"📁 Files saved to: {DATA_DIR}")
    print(f"  - {len(entries_df)} accounting entries")
    print(f"  - {len(invoices_df)} supplier invoices")
    print(f"  - {len(projects_df)} projects")
    print(f"  - {len(suppliers_df)} suppliers")


if __name__ == "__main__":
    main()
