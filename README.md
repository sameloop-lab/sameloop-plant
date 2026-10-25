# sameloop-plant — 0.1.0

**Bind & Seek — Same Control Loop, Different Embedded Stacks**

Modèle de référence proposé pour la boîte thermique, le ventilateur et son
inertie. Bibliothèque **Python**, sans dépendance runtime, sans broker et sans
contrôleur. Licence MIT. Les documentations sont en français.

## Installation et première simulation Linux

Depuis ce dépôt :

```bash
python3 -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/sameloop-plant --seconds 5 --demand 50
.venv/bin/python -m unittest discover -s tests -v
```

La simulation avance aussi vite que possible, sans attendre 5 secondes réelles.
Une ligne JSON est produite par pas. Installation initiale : accès Internet
pour le backend de construction Python. Aucun accès réseau en simulation.

## Utilisation dans un autre programme

```python
from sameloop_plant import Plant
plant = Plant()
state = plant.step(dt=0.1, demand=50.0, heat=0.18)
print(state)
```

`demand` : 0..100 %. `dt` : 0..60 secondes. `heat` : 0..2 °C/s.
Le résultat contient `temperature` (°C), `applied` (%), `rpm` (tr/min),
`elapsed` (secondes simulées). Aucun hasard, horloge système ou effet réseau.
Les entrées non finies, booléennes ou hors bornes sont refusées avant mutation.

Interface de processus, utile à un futur adaptateur C/Rust :

```bash
printf '%s\n' '{"dt":0.1,"demand":70}' '{"dt":0.1,"demand":0}' | .venv/bin/sameloop-plant --jsonl
```

Une ligne invalide produit `ok:false` et laisse l'état intact. Ce protocole
stdin/stdout n'est ni une API AFB, ni gRPC, ni un service réseau.

## Modèle et limites

Voir [le modèle](docs/MODELE.md) et [la validation](docs/VALIDATION.md).
Le choix RK4 proposé dans cette version ne modifie pas rétroactivement les UI
Flutter/LVGL ou les bindings AFB déjà livrés. Leur adaptation reste à faire :
aucune équivalence numérique avec ces anciennes implémentations n'est revendiquée.

Le contrôleur OFF/AUTO appartient à `sameloop-agl`. Le watchdog et les règles de
fraîcheur appartiennent au fournisseur, pas au modèle physique.

## Livrer

```bash
python3 -m pip install build
python3 -m build
```

La recette RPM complète se trouve dans `packaging/sameloop-plant.spec` ; elle
n'a pas été construite dans mock/OBS. Python ≥ 3.10 déclaré, Python 3.12 testé.
