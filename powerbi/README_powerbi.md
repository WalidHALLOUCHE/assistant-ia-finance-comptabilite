# Guide Power BI - Finance et Comptabilité

## Vue d'ensemble

Ce guide explique comment connecter les données CSV à Power BI et construire un dashboard professionnel pour la finance et la comptabilité.

## Architecture du modèle

### Modèle en étoile (Star Schema)

```
                     dim_date
                        |
                        |
fact_ecritures -------- |
   comptables  \        |
               \        |
                dim_compte
                
fact_factures -------- dim_fournisseur
  fournisseurs

fact_budget  -------- dim_centre_cout
                  \   |
                   dim_projet
```

## Préparation des données

### 1. Importer les CSV
1. Ouvrir Power BI Desktop
2. **Home** → **Get Data** → **Text/CSV**
3. Sélectionner chaque fichier CSV du répertoire `data/`
4. Cliquer **Load** pour charger chaque fichier

### 2. Créer les relations
**Model view** → Définir les relations :

| Relation | De | À | Clé |
|----------|----|----|-----|
| Écritures → Comptes | fact_ecritures | dim_compte_comptable | compte_id |
| Écritures → Date | fact_ecritures | dim_date | date_ecriture → date_id |
| Écritures → Centre | fact_ecritures | dim_centre_cout | centre_cout → centre_cout_id |
| Factures → Fournisseurs | fact_factures | dim_fournisseur | fournisseur_id |
| Budget → Centre | fact_budget | dim_centre_cout | centre_cout → centre_cout_id |
| Budget → Projets | fact_budget | dim_projet | Créer relation projet |

### 3. Ajouter une table de date
Si dim_date n'est pas complète :
1. **Home** → **New Table**
2. Utiliser DAX pour générer les dates manquantes

## Mesures DAX essentielles

Voir le fichier `dax_measures.md` pour les formules DAX complètes.

### Comptabilité
```
Total Débit = SUM(fact_ecritures[montant_debit])
Total Crédit = SUM(fact_ecritures[montant_credit])
Solde = [Total Débit] - [Total Crédit]
```

### Budget
```
Écart % = DIVIDE([Total Réel] - [Total Budget], [Total Budget])
Budget Consommé % = DIVIDE([Total Réel], [Total Budget])
```

### Trésorerie
```
Cash In = SUM(fact_tresorerie[cash_in])
Cash Out = SUM(fact_tresorerie[cash_out])
Solde Trésorerie = [Cash In] - [Cash Out]
```

## Construction des pages

### Page 1 : Vue DAF (Vue synthétique)
**Éléments clés** :
- KPI trésorerie (gauche)
- Graphique budget vs réel (haut)
- Tableau fournisseurs (bas)
- Indicateurs de risque

**Filtres** :
- Par mois
- Par centre de coût

### Page 2 : Comptabilité Générale
**Éléments clés** :
- Balance comptable (tableau)
- Évolution débit/crédit (graphique)
- Qualité des données (indicateurs)
- Anomalies détectées (tableau)

**Drill-down** :
- Cliquer sur un compte → détail des écritures

### Page 3 : Comptabilité Fournisseurs
**Éléments clés** :
- Top 10 fournisseurs (bar chart)
- Factures par statut (pie chart)
- Délai paiement moyen
- Factures échues (tableau)

**KPI** :
- Nombre factures
- Montant total
- Taux paiement

### Page 4 : Trésorerie
**Éléments clés** :
- Évolution solde trésorerie (line chart)
- Encaissements vs Décaissements (bar chart)
- Prévision trésorerie (line chart)
- Rapprochement bancaire (tableau)

**Indicateurs** :
- Solde actuel
- Cash position
- Jours de trésorerie

### Page 5 : Contrôle de Gestion
**Éléments clés** :
- Budget vs réel par centre (bar chart)
- Écarts budgétaires (tableau)
- Projets en dépassement (tableau)
- Tendance consommation (line chart)

**Drill-down** :
- Par centre de coût
- Par projet

### Page 6 : Qualité des Données
**Éléments clés** :
- Score qualité global (KPI)
- Anomalies par catégorie (bar chart)
- Liste des anomalies (tableau)
- Tendance qualité (line chart)

### Page 7 : Adoption IA
**Éléments clés** :
- Nombre recommandations IA
- Taux d'acceptation
- Économies générées (tempo)
- Anomalies détectées par IA

## Formatage et mise en forme

### Couleurs
- 🟢 Positif/OK : vert (#00B050)
- 🟡 Alerte : orange (#FFC000)
- 🔴 Critique : rouge (#FF0000)
- Neutre : bleu (#4472C4)

### Police
- Titre pages : 28px, Bold
- Titre section : 16px, Bold
- Texte : 11px, Regular

### Mise en avant
- KPI : Police large, couleur appropriée
- Anomalies : Mise en surbrillance rouge
- Tendances positives : Flèche ↑ verte
- Tendances négatives : Flèche ↓ rouge

## Interactivité

### Boutons de navigation
- Home → Pages principales
- Détail → Pages détail
- Retour → Page précédente

### Slicers
- Slicer mois (top)
- Slicer centre de coût (gauche)
- Slicer statut (si applicable)

### Drill-through
- Cliquer sur compte → Détail écritures
- Cliquer sur fournisseur → Détail factures
- Cliquer sur projet → Détail budget projet

## Actualisation des données

### Planification
1. **Get Data** → Options
2. Définir actualisation toutes les **heures** ou **quotidienne**
3. Configurer le service Power BI

### Source locale
Si données CSV locales :
```
Power BI → Get Data → File → Folder
Sélectionner : c:\data\finance\
```

## Export et partage

### Exporter en PDF
- File → Export → Export to PDF
- Format : A4 paysage
- Inclure dates actualisation

### Partager
- Publish → Power BI Service
- Partager avec DAF et managers
- Configurer accès par rôle (RLS)

### Rafraîchissement
- Quotidien à 8h du matin
- Actualisation manuelle possible
- Historique conservé 30 jours

## Troubleshooting

### Données non à jour
- F5 pour rafraîchir
- Home → Refresh pour re-charger
- Vérifier source CSV

### Mesure affiche "Error"
- Vérifier syntaxe DAX
- Vérifier noms colonnes
- Vérifier types de données

### Performance lente
- Réduire nombre de lignes
- Créer des agrégats
- Utiliser les filtres Slicer

## Ressources

- [DAX Guide](https://dax.guide)
- [Power BI Documentation](https://docs.microsoft.com/power-bi)
- [Fichier modèle](data_model_star_schema.md)
- [Mesures DAX](dax_measures.md)
