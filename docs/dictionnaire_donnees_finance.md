# Dictionnaire des Données Finance

## Données de Comptabilité Générale

### fact_ecritures_comptables
| Colonne | Type | Obligatoire | Description |
|---------|------|-------------|-------------|
| ecriture_id | INT | ✓ | Identifiant unique |
| date_ecriture | DATE | ✓ | Date de l'écriture |
| journal | VARCHAR(3) | ✓ | Journal (AC, VE, OP, TR) |
| numero_piece | VARCHAR(20) | ✓ | Numéro de pièce justificative |
| compte_debit | VARCHAR(10) | ✓ | Compte comptable débité |
| compte_credit | VARCHAR(10) | ✓ | Compte comptable crédité |
| montant | DECIMAL(12,2) | ✓ | Montant en euros |
| libelle | VARCHAR(255) | ✓ | Libellé de l'opération |
| centre_cout | INT | | Centre de coût |
| projet | VARCHAR(20) | | Projet |
| statut | VARCHAR(20) | | Validée, Brouillon, Pointée |

### dim_compte_comptable
| Colonne | Type | Obligatoire | Description |
|---------|------|-------------|-------------|
| compte_id | VARCHAR(10) | ✓ | Code du compte |
| compte_libelle | VARCHAR(100) | ✓ | Libellé du compte |
| classe | VARCHAR(30) | ✓ | Classe comptable (Actif, Passif, Charge, Produit) |

## Données de Gestion

### fact_budget
| Colonne | Type | Description |
|---------|------|-------------|
| budget_id | VARCHAR(20) | Identifiant |
| mois | INT | Numéro du mois |
| centre_cout | INT | Centre de coût |
| compte | VARCHAR(10) | Compte comptable |
| budget | DECIMAL(12,2) | Montant budgété |
| reel | DECIMAL(12,2) | Montant réalisé |
| ecart | DECIMAL(12,2) | Écart (reel - budget) |

### fact_factures_fournisseurs
| Colonne | Type | Description |
|---------|------|-------------|
| facture_id | VARCHAR(20) | Identifiant unique |
| fournisseur_id | VARCHAR(20) | Identifiant fournisseur |
| date_facture | DATE | Date de facturation |
| date_echeance | DATE | Date d'échéance |
| montant_ht | DECIMAL(12,2) | Montant HT |
| tva_montant | DECIMAL(12,2) | Montant TVA |
| montant_ttc | DECIMAL(12,2) | Montant TTC |
| statut | VARCHAR(20) | Payée, Impayée, Échue |
| date_paiement | DATE | Date de paiement |
| compte_charge | VARCHAR(10) | Compte de charge |
| reference | VARCHAR(50) | Référence facture |

## Données de Trésorerie

### fact_tresorerie
| Colonne | Type | Description |
|---------|------|-------------|
| tresorerie_id | VARCHAR(20) | Identifiant |
| date | DATE | Date du mouvement |
| cash_in | DECIMAL(12,2) | Encaissements |
| cash_out | DECIMAL(12,2) | Décaissements |
| solde | DECIMAL(12,2) | Solde de trésorerie |

### fact_rapprochement_bancaire
| Colonne | Type | Description |
|---------|------|-------------|
| rapprochement_id | VARCHAR(20) | Identifiant |
| date_ecriture | DATE | Date de l'écriture |
| date_mouvement_bancaire | DATE | Date du mouvement banque |
| montant_ecriture | DECIMAL(12,2) | Montant comptable |
| montant_banque | DECIMAL(12,2) | Montant bancaire |
| statut | VARCHAR(20) | Rapproché, Non rapproché |
| description | VARCHAR(255) | Description |

## Données de Dimension

### dim_centre_cout
| Colonne | Type | Description |
|---------|------|-------------|
| centre_cout_id | INT | Identifiant |
| centre_cout | VARCHAR(50) | Libellé |
| responsable | VARCHAR(100) | Responsable |

### dim_projet
| Colonne | Type | Description |
|---------|------|-------------|
| projet_id | VARCHAR(20) | Identifiant |
| projet_nom | VARCHAR(100) | Nom du projet |
| region | VARCHAR(50) | Région |
| capacite_mwc | DECIMAL(8,2) | Capacité en MWc |
| date_debut | DATE | Date de début |
| statut | VARCHAR(20) | En cours, Terminé, Planifié |
| budget_total | DECIMAL(12,2) | Budget total |

### dim_fournisseur
| Colonne | Type | Description |
|---------|------|-------------|
| fournisseur_id | VARCHAR(20) | Identifiant |
| fournisseur_nom | VARCHAR(100) | Nom |
| type | VARCHAR(50) | Type (Équipementier, etc.) |
| siret | VARCHAR(14) | SIRET |
| adresse | VARCHAR(255) | Adresse |
| pays | VARCHAR(50) | Pays |
| email | VARCHAR(100) | Email |

### dim_date
| Colonne | Type | Description |
|---------|------|-------------|
| date_id | VARCHAR(8) | Format YYYYMMDD |
| date | DATE | Date |
| year | INT | Année |
| month | INT | Mois |
| month_name | VARCHAR(20) | Nom mois |
| day | INT | Jour |
| week | INT | Semaine |
| quarter | INT | Trimestre |

## Conventions de nommage
- **Tables de faits** : Préfixe `fact_`
- **Tables de dimension** : Préfixe `dim_`
- **Dates** : Format ISO (YYYY-MM-DD)
- **Montants** : DECIMAL(12,2) pour 2 décimales
- **Identifiants** : Préfixe du type (PROJ_, SUPP_, etc.)
