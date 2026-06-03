# Mesures DAX Power BI Finance

## Comptabilité Générale

### Totaux Débit/Crédit
```dax
Montant Débit = 
SUMIF(
    fact_ecritures,
    fact_ecritures[compte_debit],
    fact_ecritures[montant]
)

Montant Crédit = 
SUMIF(
    fact_ecritures,
    fact_ecritures[compte_credit],
    fact_ecritures[montant]
)
```

### Solde Comptable
```dax
Solde Comptable = 
VAR debit = [Montant Débit]
VAR credit = [Montant Crédit]
RETURN debit - credit
```

### Équilibre Débit/Crédit
```dax
Est Équilibré = 
IF(
    ABS([Montant Débit] - [Montant Crédit]) < 0.01,
    "Oui",
    "Non"
)
```

## Budget et Réel

### Total Budget
```dax
Total Budget = SUM(fact_budget[budget])
```

### Total Réel
```dax
Total Réel = SUM(fact_budget[reel])
```

### Écart Budget/Réel
```dax
Écart = [Total Réel] - [Total Budget]
```

### Écart en %
```dax
Écart % = 
DIVIDE(
    [Écart],
    [Total Budget],
    0
) * 100
```

### Budget Consommé %
```dax
Budget Consommé % = 
DIVIDE(
    [Total Réel],
    [Total Budget],
    0
) * 100
```

### Indicateur Statut
```dax
Statut Budget = 
VAR ecart = ABS([Écart %])
RETURN
    IF(
        ecart <= 5,
        "🟢 Conforme",
        IF(
            ecart <= 10,
            "🟡 À surveiller",
            "🔴 Dépassement"
        )
    )
```

## Comptabilité Fournisseurs

### Total Factures
```dax
Total Factures = COUNTA(fact_factures_fournisseurs[facture_id])
```

### Montant Total Facturé
```dax
Montant Total = SUM(fact_factures_fournisseurs[montant_ttc])
```

### Factures Payées
```dax
Factures Payées = 
COUNTIF(
    fact_factures_fournisseurs,
    fact_factures_fournisseurs[statut] = "Payée"
)
```

### Factures Non Payées
```dax
Factures Non Payées = 
[Total Factures] - [Factures Payées]
```

### Factures Échues
```dax
Factures Échues = 
COUNTIFS(
    fact_factures_fournisseurs,
    fact_factures_fournisseurs[date_echeance] < TODAY(),
    fact_factures_fournisseurs,
    fact_factures_fournisseurs[statut] <> "Payée"
)
```

### Montant Factures Échues
```dax
Montant Échues = 
SUMIFS(
    fact_factures_fournisseurs[montant_ttc],
    fact_factures_fournisseurs[date_echeance], < TODAY(),
    fact_factures_fournisseurs[statut], <> "Payée"
)
```

### Délai Moyen de Paiement
```dax
Délai Moyen Paiement = 
AVERAGEX(
    FILTER(
        fact_factures_fournisseurs,
        fact_factures_fournisseurs[statut] = "Payée"
    ),
    DATEDIFF(
        fact_factures_fournisseurs[date_facture],
        fact_factures_fournisseurs[date_paiement],
        DAY
    )
)
```

## Trésorerie

### Cash In
```dax
Cash In = SUM(fact_tresorerie[cash_in])
```

### Cash Out
```dax
Cash Out = SUM(fact_tresorerie[cash_out])
```

### Solde Trésorerie
```dax
Solde Trésorerie = [Cash In] - [Cash Out]
```

### Solde Courant
```dax
Solde Courant = 
LASTNONBLANK(
    fact_tresorerie[solde],
    fact_tresorerie[solde]
)
```

### Position Liquidité
```dax
Position Liquidité = 
IF(
    [Solde Courant] > 500000,
    "🟢 Excellent",
    IF(
        [Solde Courant] > 100000,
        "🟡 Normal",
        "🔴 Critique"
    )
)
```

## Qualité des Données

### Nombre Anomalies
```dax
Anomalies = 
VAR missing_center = 
    COUNTBLANK(fact_ecritures[centre_cout])
VAR invalid_accounts = 
    COUNTIF(fact_ecritures[compte_debit], <dim_compte[compte_id])
RETURN missing_center + invalid_accounts
```

### Score Qualité
```dax
Score Qualité = 
VAR total_records = ROWS(fact_ecritures)
VAR anomalies = [Anomalies]
RETURN
    IF(
        total_records = 0,
        0,
        (total_records - anomalies) / total_records * 100
    )
```

### Statut Qualité
```dax
Statut Qualité = 
VAR score = [Score Qualité]
RETURN
    IF(
        score >= 95,
        "🟢 Excellente",
        IF(
            score >= 85,
            "🟡 Acceptable",
            "🔴 Problèmes"
        )
    )
```

## Mesures Composites

### Performance Générale
```dax
Performance = 
VAR budget_ok = IF([Écart %] <= 10, 1, 0)
VAR tresorerie_ok = IF([Solde Courant] > 100000, 1, 0)
VAR qualite_ok = IF([Score Qualité] >= 90, 1, 0)
RETURN (budget_ok + tresorerie_ok + qualite_ok) / 3 * 100
```

### Alertes Critiques
```dax
Alertes Critiques = 
VAR alerte_budget = IF(ABS([Écart %]) > 15, 1, 0)
VAR alerte_factures = IF([Factures Échues] > 5, 1, 0)
VAR alerte_qualite = IF([Score Qualité] < 80, 1, 0)
RETURN alerte_budget + alerte_factures + alerte_qualite
```

## Mesures Comparatives

### Variation Mois Précédent
```dax
Variation MoM = 
VAR current = [Total Réel]
VAR previous = 
    CALCULATE(
        [Total Réel],
        DATEADD(dim_date[date], -1, MONTH)
    )
RETURN DIVIDE(current - previous, previous, 0) * 100
```

### Variation Année Précédente
```dax
Variation YoY = 
VAR current = [Total Réel]
VAR previous = 
    CALCULATE(
        [Total Réel],
        DATEADD(dim_date[date], -1, YEAR)
    )
RETURN DIVIDE(current - previous, previous, 0) * 100
```
