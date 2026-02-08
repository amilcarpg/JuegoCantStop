# Bots requeridos

Todos los bots implementan:
- choose_move(state, dice, legal_moves) -> move
- decide_stop(state, rolls_this_turn) -> bool

## Bot base: AlwaysContinue
- choose_move: puede ser aleatorio o simple, pero preferible determinista (elegir primer move ordenado).
- decide_stop: siempre False (solo para si gana al bank, pero este bot nunca banquea por decisión; solo termina por bust).

## Bot: MaxNRolls(N)
- decide_stop: True cuando rolls_this_turn >= N.
- choose_move: preferible usar GreedyConservative (para estabilidad) o un selector determinista.

## GreedyAggressive (G_A)
### Intención
Maximiza completar columnas pronto, acepta abrir columnas nuevas y tomar riesgos implícitos.

### choose_move scoring
Para cada move candidato:
1. Simular aplicar move sobre un estado-copia (sin cambiar el original).
2. Score = suma por cada columna tocada:
   - base = (permanent[col] + temp[col]) / altura[col]
3. Bonus fuerte si la columna llega a completarse al bank:
   - Si después del move, (permanent + temp) >= altura => bonus +B (B grande, ej 2.0).
4. Bonus adicional si con el bank actual se completaría la 3ra columna (condición de victoria inminente) => +W (W > B).
5. Tie-breakers deterministas:
   - preferir moves que avancen 2 pasos (x,x) si score igual
   - luego preferir mayor suma de columnas (más alto) o menor, pero fijo (definir un orden estable).

### decide_stop
- Por defecto: parar si con bank ahora se gana (3 columnas).
- En caso contrario: NO decide parar (se usa con política externa como MaxNRolls o RiskStop).

## GreedyConservative (G_C)
### Intención
Minimiza riesgo de bust indirectamente: evita abrir columnas nuevas si no hace falta y favorece consolidar columnas activas.

### choose_move scoring
Para cada move candidato:
1. Simular aplicar move.
2. Score base similar: sum((perm+temp)/altura) para columnas tocadas.
3. Penalización por abrir una columna nueva:
   - si el move abre una columna no activa => score -= P (P significativo, ej 0.5 a 1.0)
4. Bonus por mover en columnas ya activas (consolidación):
   - por cada columna en move que ya era activa => score += A (pequeño, ej 0.1)
5. Bonus por completado al bank:
   - bonus +B (menor que el agresivo, pero existe)
6. Tie-breakers deterministas:
   - preferir NO abrir columna nueva
   - preferir moves de una sola columna sobre dos si score igual (reduce exposición futura)
   - orden estable por columna.

### decide_stop
- Por defecto: parar si con bank se gana.
- Si no: no para (se combina con MaxNRolls o RiskStop).

## (Opcional recomendado) RiskStop(T) wrapper
- Usa un "move policy" interna (G_C o G_A) para choose_move.
- decide_stop:
  - Calcula P(bust | estado actual) enumerando todas las 1296 tiradas.
  - Si P(bust) >= T => True, si no False.
  - Siempre True si con bank se gana.
- Debe ser determinista y eficiente (cache por patrón de columnas activas y posiciones si aplica).
