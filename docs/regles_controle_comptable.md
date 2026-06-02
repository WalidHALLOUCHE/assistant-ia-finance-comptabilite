# Règles de Contrôle Comptable

## Contrôles d'équilibre

### Règle 1 : Équilibre débit/crédit
**Condition** : Pour chaque écriture, Débit = Crédit  
**Action si violation** : Bloquer la validation de l'écriture  
**Message** : "L'écriture n'est pas équilibrée. Débit ≠ Crédit"

### Règle 2 : Équilibre par journal
**Condition** : Pour chaque journal, Total Débits = Total Crédits  
**Périodicité** : Mensuelle  
**Tolérance** : 0€  

### Règle 3 : Balance équilibrée
**Condition** : Total actif = Total passif + capitaux propres  
**Périodicité** : En clôture  

## Contrôles de validité

### Règle 4 : Compte comptable valide
**Condition** : Le compte doit exister dans le plan comptable  
**Action si violation** : Alerte et proposition de correction

### Règle 5 : Centre de coût obligatoire
**Condition** : Toutes les charges doivent avoir un centre de coût  
**Exceptions** : Écritures de provisions, dotations aux amortissements  
**Action si violation** : Alerte

### Règle 6 : Projet obligatoire si applicable
**Condition** : Si frais de projet, alors projet_id doit être rempli  
**Action si violation** : Alerte

## Contrôles de plausibilité

### Règle 7 : Montants raisonnables
**Condition** : Pas de montant > 500K€ sans justification  
**Action si violation** : Alerte

### Règle 8 : Dates cohérentes
**Condition** : Date écriture >= Date pièce justificative  
**Condition** : Date écriture <= Date du jour + 5 jours  
**Action si violation** : Alerte

### Règle 9 : Libellé obligatoire
**Condition** : Libellé rempli et > 3 caractères  
**Action si violation** : Alerte

## Contrôles de cohérence

### Règle 10 : Cohérence compte 512 (Banque)
**Condition** : Solde compte 512 = Solde relevé bancaire  
**Tolérance** : ± 5€  
**Périodicité** : Mensuelle

### Règle 11 : Cohérence clients/fournisseurs
**Condition** : Factures clients = solde compte 411  
**Condition** : Factures fournisseurs = solde compte 401  

### Règle 12 : Délai de paiement standard
**Condition** : Factures fournisseurs payées dans les 45 jours  
**Alerte si** : Facture impayée > 60 jours

## Contrôles d'anomalies

### Règle 13 : Pas de doublon
**Condition** : Une pièce justificative = Une seule écriture comptable  
**Détection** : Même numéro de pièce avec même montant

### Règle 14 : Pas d'écriture en brouillon en clôture
**Condition** : Tous les statuts = "Validée" ou "Pointée"  
**Périodicité** : En clôture

### Règle 15 : Délai de saisie
**Condition** : Écriture comptabilisée dans les 3 jours  
**Alerte si** : Délai > 5 jours

## Matrice de sévérité

| Sévérité | Définition | Action |
|----------|-----------|--------|
| 🔴 Critique | Bloque la clôture | Correction immédiate |
| 🟠 Majeure | Impact significatif | Correction avant signature |
| 🟡 Mineure | À améliorer | Correction recommandée |
| 🟢 Info | À titre informatif | Suivi |

## Procédure de validation

1. **Saisie** : Contrôles à la saisie (R4, R5, R6, R9)
2. **Détail** : Contrôles en détail (R7, R8, R13)
3. **Mensuel** : Contrôles mensuels (R1, R2, R3, R11, R12)
4. **Clôture** : Contrôles de clôture (R3, R14)
