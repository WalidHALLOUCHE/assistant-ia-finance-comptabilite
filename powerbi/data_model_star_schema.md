# Modèle de Données Star Schema

## Architecture

Le modèle de données suit une architecture en étoile (star schema) optimisée pour Power BI et l'analytique financière.

## Tables de Faits

### 1. fact_ecritures_comptables
**Granularité** : Une ligne = Une écriture comptable

| Colonne | Type | Clé | Utilisation |
|---------|------|-----|-------------|
| ecriture_id | INT | PK | Identifiant unique |
| date_ecriture | DATE | FK | Lien vers dim_date |
| compte_debit | VARCHAR | FK | Lien vers dim_compte |
| compte_credit | VARCHAR | FK | Lien vers dim_compte |
| montant | DECIMAL | | Mesure |
| centre_cout | INT | FK | Lien vers dim_centre |
| projet | VARCHAR | FK | Lien vers dim_projet |

**Mesures principales** :
- SUM(montant) → Total débits/crédits
- COUNT(ecriture_id) → Nombre écritures

### 2. fact_factures_fournisseurs
**Granularité** : Une ligne = Une facture fournisseur

| Colonne | Type | Clé |
|---------|------|-----|
| facture_id | VARCHAR | PK |
| fournisseur_id | VARCHAR | FK |
| date_facture | DATE | FK |
| date_echeance | DATE | FK |
| montant_ttc | DECIMAL | Mesure |
| statut | VARCHAR | Dimension |

**Mesures principales** :
- SUM(montant_ttc) → Total facturé
- COUNT(facture_id) → Nombre factures
- COUNTIF(statut="Payée") → Factures payées

### 3. fact_budget
**Granularité** : Une ligne = Un budget mensuel par centre/compte

| Colonne | Type |
|---------|------|
| budget_id | VARCHAR |
| mois | INT |
| centre_cout | INT |
| compte | VARCHAR |
| budget | DECIMAL |
| reel | DECIMAL |

### 4. fact_tresorerie
**Granularité** : Une ligne = Un jour de trésorerie

| Colonne | Type |
|---------|------|
| date | DATE |
| cash_in | DECIMAL |
| cash_out | DECIMAL |
| solde | DECIMAL |

### 5. fact_rapprochement_bancaire
**Granularité** : Une ligne = Un rapprochement

| Colonne | Type |
|---------|------|
| montant_ecriture | DECIMAL |
| montant_banque | DECIMAL |
| statut | VARCHAR |

## Tables de Dimension

### 1. dim_date
**Rôle** : Référence temporelle unique

| Colonne | Type | Utilisation |
|---------|------|-------------|
| date_id | VARCHAR(8) | Clé primaire (YYYYMMDD) |
| date | DATE | Affichage |
| year | INT | Filtrage |
| month | INT | Filtrage |
| month_name | VARCHAR | Affichage |
| quarter | INT | Agrégation |
| week | INT | Agrégation |

**Raison** : Une dim_date unique assure la cohérence des filtres temporels.

### 2. dim_compte_comptable
**Rôle** : Référence plans comptables

| Colonne | Type |
|---------|------|
| compte_id | VARCHAR(10) |
| compte_libelle | VARCHAR(100) |
| classe | VARCHAR(30) |

**Hiérarchie** :
- Classe (Actif, Passif, Charge, Produit)
  - Compte parent (401, 411, etc.)
    - Compte détail (401110, 411001, etc.)

### 3. dim_centre_cout
**Rôle** : Structures organisationnelles

| Colonne | Type |
|---------|------|
| centre_cout_id | INT |
| centre_cout | VARCHAR(50) |
| responsable | VARCHAR(100) |

### 4. dim_projet
**Rôle** : Projets et programmes

| Colonne | Type |
|---------|------|
| projet_id | VARCHAR(20) |
| projet_nom | VARCHAR(100) |
| region | VARCHAR(50) |
| capacite_mwc | DECIMAL |
| statut | VARCHAR(20) |
| budget_total | DECIMAL |

### 5. dim_fournisseur
**Rôle** : Référentiel fournisseurs

| Colonne | Type |
|---------|------|
| fournisseur_id | VARCHAR(20) |
| fournisseur_nom | VARCHAR(100) |
| type | VARCHAR(50) |
| siret | VARCHAR(14) |
| pays | VARCHAR(50) |

## Relations clés

### Relation 1 : Écritures → Comptes
```
fact_ecritures.compte_debit → dim_compte_comptable.compte_id
Cardinalité : Many-to-One
```

### Relation 2 : Écritures → Date
```
fact_ecritures.date_ecriture → dim_date.date_id
Cardinalité : Many-to-One
```

### Relation 3 : Écritures → Centre
```
fact_ecritures.centre_cout → dim_centre_cout.centre_cout_id
Cardinalité : Many-to-One
```

### Relation 4 : Factures → Fournisseurs
```
fact_factures_fournisseurs.fournisseur_id → dim_fournisseur.fournisseur_id
Cardinalité : Many-to-One
```

### Relation 5 : Budget → Centre
```
fact_budget.centre_cout → dim_centre_cout.centre_cout_id
Cardinalité : Many-to-One
```

## Types de données recommandés

```
Dates : DATE (pas DATETIME)
Montants : DECIMAL(12,2)
Codes : VARCHAR
Textes : VARCHAR(255+)
Identifiants : INTEGER ou VARCHAR
Booléens : VARCHAR("Oui"/"Non")
```

## Optimisations

### 1. Partitionnement par date
Diviser les tables de faits par année/mois pour optimiser :
```
fact_ecritures_2024_01
fact_ecritures_2024_02
...
```

### 2. Agrégats pré-calculés
Créer des mesures agrégées pour les rapports courants :
```
Somme mensuelle par centre
Factures par statut
Budget par projet
```

### 3. Index sur clés
Créer des index sur :
- Clés primaires/étrangères
- Colonnes de filtrage fréquent
- Colonnes temporelles

## Cardinalité des relations

| De | À | Cardinalité | Exemple |
|----|----|-------------|---------|
| fact_ecritures | dim_compte | Many-to-One | 1000 écritures → 50 comptes |
| fact_factures | dim_fournisseur | Many-to-One | 500 factures → 30 fournisseurs |
| fact_budget | dim_centre | Many-to-One | 200 budgets → 10 centres |

## Modèle logique complet

```
dim_date ◄──────┬──────────────────────┐
                 |                      |
                 │                      │
         fact_ecritures ────► dim_compte
            ◄──────┬                    
                   │         dim_centre_cout
                   │              ▲
                   │              │
                   └──────────────┘
                   
fact_factures ────► dim_fournisseur
  │
  ▼
dim_date

fact_budget ────► dim_centre_cout
  │
  ▼
dim_date

fact_tresorerie ────► dim_date

fact_rapprochement ────► dim_date
```
