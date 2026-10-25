# Validation — 25 octobre 2026

Version 0.1.0 ; Linux x86_64, Python 3.12.14.

- 6 tests unitaires exécutés et réussis : solutions analytiques thermique/fan,
  partition temporelle, refus atomique des valeurs invalides, inertie, pas nul.
- Wheel et archive source construites avec setuptools 84.2.1 / build 1.6.1.
- Modèle utilisé par le fournisseur dans les tests KUKSA réels de sameloop-agl.

Le journal unitaire est dans `unit-results.txt`. Reproduction :
`python -m unittest discover -s tests -v`.

Non testé : RPM/mock/OBS, Fedora utilisateur, aarch64, intégration Flutter/LVGL,
réutilisation dans AFB et matériel. Les tests analytiques valident ce modèle,
pas la fidélité physique à un équipement réel.
