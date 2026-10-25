# Modèle de référence 0.1.0

État initial : température 32,4 °C, ventilation appliquée 0 %, vitesse 0 tr/min.
Ambiance : 20 °C. Entrées : commande u (%), apport thermique H (°C/s).

```text
dT/dt   = H - (0.015 + 0.12 × a / 100) × (T - 20)
da/dt   = (u - a) / 0.6
drpm/dt = (40 × a - rpm) / 0.8
```

Intégration couplée Runge-Kutta d'ordre 4, pas interne au plus 10 ms :
`n=ceil(dt/0.01)`, `h=dt/n`. L'entrée reste constante pendant un appel.
Un pas externe usuel vaut 100 ms. L'intégration n'utilise pas le temps mur.
Les résultats sont reproductibles à tolérance flottante, pas garantis identiques
bit à bit entre toutes architectures et toutes bibliothèques mathématiques.

Deux cas analytiques servent de référence indépendante dans les tests :
refroidissement sans ventilation et cascade de deux filtres du ventilateur.
Le test par partition compare 1 seconde à dix pas de 100 ms.

H normal vaut 0,18 ; la perturbation de chauffe vaut 1,2. C'est une maquette,
pas la calibration d'une enceinte ou d'un moteur industriel. La température
n'est pas artificiellement ramenée à la consigne par le simulateur.
