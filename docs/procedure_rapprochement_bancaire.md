# Procédure Rapprochement Bancaire

## Objectif
Documenter le processus de rapprochement entre les écritures comptables et les mouvements bancaires.

## Fréquence
- **Rapprochement quotidien** : Pour les comptes importants
- **Rapprochement mensuel** : Au minimum pour tous les comptes

## Processus de rapprochement

### Étape 1 : Extraction des données
1. Exporter la liste des écritures comptables du mois (compte 512 Banque)
2. Télécharger les relevés bancaires auprès de chaque établissement
3. Vérifier la cohérence des soldes d'ouverture/fermeture

### Étape 2 : Pointage des écritures
1. Associer chaque mouvement bancaire à une écriture comptable
2. Vérifier :
   - La concordance des montants
   - La concordance des dates (avec tolérance de 2 jours)
   - La description/libellé cohérent

### Étape 3 : Identification des écarts
Les écarts peuvent être de plusieurs natures :

#### A. Écarts de montant
- **Cause fréquente** : Frais bancaires non comptabilisés
- **Action** : Générer une écriture de régularisation

#### B. Écarts de date
- **Cause fréquente** : Délai de virement/chèque
- **Tolérance** : 3 jours maximum
- **Action** : Accepter l'écart si dans la tolérance

#### C. Mouvements bancaires non identifiés
- **Cause fréquente** : Virements entrants, remboursements
- **Action** : Rechercher l'écriture comptable correspondante

#### D. Écritures comptables non pointées
- **Cause fréquente** : Chèques non encaissés, virements en cours
- **Action** : Suivre la date d'encaissement/virement

### Étape 4 : Régularisations
Générer les écritures manquantes :
- Frais bancaires
- Intérêts bancaires
- Escomptes reçus
- Différences de change

### Étape 5 : Validation
- [ ] Tous les mouvements bancaires sont pointés
- [ ] Tous les écarts sont expliqués
- [ ] Les régularisations sont enregistrées
- [ ] Le solde comptable = solde bancaire

## Exemple de tableau de rapprochement

| Date | Libellé | Montant Comptable | Montant Bancaire | Pointé | Écart |
|------|---------|------------------|------------------|--------|-------|
| 01/01 | Chèque fournisseur | 5000 | 5000 | ✓ | 0 |
| 02/01 | Virement client | 15000 | 15000 | ✓ | 0 |
| 03/01 | Frais bancaires | 50 | 50 | ✓ | 0 |

## Indicateurs clés
- **Taux de rapprochement** : Objectif 100%
- **Délai de régularisation** : < 5 jours
- **Écarts non expliqués** : 0 toléré

## Documents à archiver
- Relevés bancaires originaux
- Liste d'écritures comptables
- Tableau de rapprochement
- Écritures de régularisation
