# Criterios de aceptación

1) El motor implementa EXACTAMENTE las reglas en SPEC.md.
2) Los bots GreedyAggressive y GreedyConservative siguen BOTS.md con desempates deterministas.
3) Se puede correr un batch de N partidas con seed controlado y obtener métricas.
4) Suite de tests pasa:
   - unitarios de reglas
   - determinismo de partida
   - test repetitivo con X repeticiones (configurable)
5) No hay UI.
6) Código claro, tipado (typing) y modular.
