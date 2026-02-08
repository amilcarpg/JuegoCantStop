# Testing y validación (obligatorio)

## Framework
Usar unittest o pytest (preferible pytest si está permitido; si no, unittest).

## Principios
- Tests deterministas con seed fijo.
- No depender de azar no controlado.
- En tests estadísticos, usar tolerancias/rangos para evitar flakiness.

## Tests unitarios de reglas
1) pairings:
- Para una tupla de dados fija, debe devolver exactamente 3 particiones correctas.
2) legal_moves:
- Caso con 0 columnas activas y <3 activas: debe permitir abrir nuevas.
- Caso con 3 activas: NO permitir abrir 4ta.
- Caso con columna completada: NO permitir mover en esa columna.
- Caso (x,x): debe representar +2 en la misma columna.
3) bust:
- Si legal_moves vacío, al aplicar bust: temp debe quedar vacío y active_cols vacío.
4) bank:
- Al bank, temp se suma a permanente, y se resetea temp/active_cols.
- Debe marcar columna completada al alcanzar altura.
5) win condition:
- Al completar 3 columnas tras bank, debe declarar ganador.

## Test determinista de partida
- Configurar 4 bots simples (por ejemplo, MaxNRolls(2) con choose_move determinista).
- Con seed fijo, el ganador (índice) debe ser reproducible.
- También verificar que la partida termina (no loop infinito) en un máximo razonable de turnos.

## Test "X repeticiones" como prueba unitaria (requerido)
Objetivo: asegurar estabilidad del motor y detectar regresiones.

- Definir X configurable por env var o constante (por defecto X=200 o X=500 para CI rápido).
- Ejecutar X partidas con seed base fijo (por ejemplo seed=12345) y seeds derivados (seed+i).
- Composición de mesa sugerida:
  - [GreedyConservative+MaxNRolls(3), GreedyAggressive+MaxNRolls(3), MaxNRolls(2), RandomDeterministic]
- Métricas a validar con tolerancia:
  1) Suma de victorias = X
  2) Win-rate de G_A y G_C dentro de un rango esperado (definir rangos amplios al inicio):
     - Ejemplo inicial: cada bot entre 10% y 40% para X=500 (evita flakiness).
  3) Bust-rate promedio dentro de rango razonable (ej 0.10 a 0.60).
  4) Duración promedio en turnos dentro de rango (ej 30 a 300).
- Importante: elegir rangos suficientemente amplios para que el test no falle por ruido pero sí por bugs severos.

## Nota sobre performance
Enumerar 1296 tiradas para RiskStop puede ser costoso. Para tests, usar bots sin RiskStop o bajar X.
