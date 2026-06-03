# Spécification des Dashboards Power BI

## Page 1 : Vue DAF (Executive Dashboard)

### Objectif
Donner une vue synthétique et rapide de la situation financière à la DAF.

### Disposition
```
┌─────────────────────────────────────────────────────┐
│  Vue DAF - {Mois} {Année}                [Filtres]  │
├────────────┬────────────────┬──────────────────────┤
│ KPI Colonne│  Analyse       │ Graphiques           │
│            │                │                      │
│ 🟢 Tréso   │ Budget vs Réel │ Top Fournisseurs    │
│ 🟡 Budget  │ (Line chart)   │ (Horizontal bar)    │
│ 🟢 Qualité │                │                      │
└────────────┴────────────────┴──────────────────────┘
```

### Éléments
- **KPI Trésorerie** : Solde courant avec tendance (↑/↓)
- **KPI Budget** : Écart % avec statut (🟢/🟡/🔴)
- **KPI Qualité** : Score qualité données
- **Budget vs Réel** : Line chart mensuelle
- **Top Fournisseurs** : Top 5 par montant
- **Alertes** : Tableau des alertes critiques

### Filtres
- Slicer Mois
- Slicer Centre de Coût

---

## Page 2 : Comptabilité Générale

### Objectif
Détail complet de la comptabilité générale et validation.

### Sections

#### Section A : Balance
- Tableau complet compte | Débit | Crédit | Solde
- Filtrable par classe comptable
- Drill-down vers écritures détail

#### Section B : Analyse
- Évolution débit vs crédit (line chart)
- Soldes par classe (stacked bar)
- Distribution écritures (pie)

#### Section C : Contrôle qualité
- Écritures non équilibrées : COUNT
- Écritures sans centre : COUNT
- Écritures en brouillon : COUNT
- Score équilibre : %

#### Section D : Tableau détail
- Filtrable par statut
- Drill-through vers pièce justificative
- Export Excel

### KPI
- ✅ Équilibre : Oui/Non
- 📊 Nombre écritures : {N}
- 🔴 Anomalies : {N}

---

## Page 3 : Comptabilité Fournisseurs

### Objectif
Suivi des factures fournisseurs et trésorerie payable.

### Sections

#### Section A : Synthèse
```
Total Factures: 125
Montant: 850K€
Payées: 75 (60%)
Échues: 12 (9.6%)
```

#### Section B : Analyses
- **Top 10 Fournisseurs** : Horizontal bar chart
- **Factures par Statut** : Pie chart (Payée/Impayée/Échue)
- **Délai Paiement** : Line chart historique

#### Section C : Risque Crédit
- Tableau fournisseurs échues :
  - Fournisseur | Montant | Jours écoulés | Action
- Montant total à risque : KPI

#### Section D : Tendances
- Charges mensuelles par fournisseur (stacked area)
- Évolution délai de paiement (line)

### Drill-down
- Cliquer fournisseur → Détail factures
- Cliquer facture → Pièce jointe/Notes

---

## Page 4 : Trésorerie

### Objectif
Suivi détaillé de la trésorerie et prévisions.

### Sections

#### Section A : Situation
```
Solde Actuel: 250K€ 🟢
Cash In: 500K€ ↑
Cash Out: 350K€ ↓
Position: Excellent
```

#### Section B : Graphiques
- **Évolution Solde** : Line chart (3 mois)
- **Cash Flow** : Waterfall chart
- **Prévision 30j** : Forecast line

#### Section C : Rapprochement Bancaire
- Tableau complet
- Statut rapprochement : ✓ / ✗
- Écarts détectés
- Taux rapprochement : %

#### Section D : Mouvements
- Encaissements derniers jours (tableau)
- Décaissements prévus (tableau)
- Alertes liqui dité

### KPI
- 💰 Liquidité position
- 📈 Tendance
- ✅ Réconciliation rate

---

## Page 5 : Contrôle de Gestion

### Objectif
Suivi budget vs réel et analyse écarts.

### Sections

#### Section A : Synthèse Budget
```
Budget Total: 2M€
Réel: 2.1M€
Écart: +100K€ (+5%)
Statut: 🟡 À surveiller
```

#### Section B : Analyses Détail
- **Budget vs Réel par Centre** : Cluster column chart
- **Consommation Budget** : Gauge chart (%)
- **Top Écarts** : Sorted bar chart

#### Section C : Projets
- Performance par projet (tableau)
- Dépassements budgétaires (table)
- Rentabilité par MW (scatter)

#### Section D : Tendances
- Évolution écarts (line)
- Budget consommé % (line)
- Projection end-of-month (trend)

### Drill-down
- Par centre de coût
- Par projet
- Par compte

---

## Page 6 : Qualité des Données

### Objectif
Monitoring et amélioration de la qualité des données.

### Sections

#### Section A : Score Global
```
Score: 92% 🟢
Anomalies: 48
Tendance: ↑ (+2%)
```

#### Section B : Anomalies par Catégorie
- **Nombre par type** : Stacked bar
  - Sans centre de coût : X
  - Sans date échéance : X
  - Montants invalides : X
  - Doublons : X
  - Autres : X

#### Section C : Détail Anomalies
Tableau filtrable :
- Type | Nombre | % du total | Sévérité | Recommandation

#### Section D : Historique
- Tendance score qualité (line)
- Anomalies fermées vs ouvertes (area chart)
- Taux résolution (%)

### KPI
- 🎯 Score qualité
- 🔴 Critiques
- ⏱️ Temps moyen résolution

---

## Page 7 : Adoption IA

### Objectif
Mesurer l'utilisation et impact de l'IA.

### Sections

#### Section A : Utilisation
```
Recommandations: 128
Acceptées: 110 (86%)
Rejetées: 18 (14%)
Économies: 15h
```

#### Section B : Impact
- **Anomalies Détectées** : Line chart
- **Temps Gagné** : Bar chart (heures/mois)
- **Taux d'Erreur** : Gauge (avant vs après)

#### Section C : Par Domaine
Tableau :
- Comptabilité
- Fournisseurs
- Trésorerie
- Contrôle gestion

#### Section D : Recommandations Acceptées
- Tableau détail
- Justification
- Résultat

### KPI
- 📊 Taux d'acceptation
- ⏱️ Heures économisées
- 🎯 Amélioration qualité

---

## Éléments Communs à Toutes les Pages

### En-tête
- Nom page
- Filtre mois (Slicer date)
- Date actualisation
- Boutton Home

### Pied de page
- "Confidentiel - Finance"
- Numéro page
- Lien documentation

### Filtres Globaux
- Slicer Mois : Depuis {N} mois
- Slicer Centre Coût : Multiple
- Slicer Projet : Multiple

### Couleurs Standards
- Positif : Vert (#00B050)
- Alerte : Orange (#FFC000)
- Critique : Rouge (#FF0000)
- Neutre : Gris (#808080)

### Navigation
- Boutons précédent/suivant
- Index des pages
- Lien recherche
