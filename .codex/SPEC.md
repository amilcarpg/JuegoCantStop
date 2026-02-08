# Can't Stop (clásico) — Especificación de simulación (4 jugadores)

## Tablero
Columnas 2..12. Alturas estándar:
2:3, 3:5, 4:7, 5:9, 6:11, 7:13, 8:11, 9:9, 10:7, 11:5, 12:3.

## Componentes por jugador
- Progreso permanente por columna (0..altura).
- Columnas completadas (cuando permanente >= altura).
- Objetivo: completar 3 columnas.

## Turno
- Se tiran 4 dados (d1..d4).
- Se forman 2 pares; hay 3 particiones posibles:
  (d1+d2, d3+d4), (d1+d3, d2+d4), (d1+d4, d2+d3).
- En cada tirada, el jugador elige una partición y, dentro de ella, decide mover:
  - Si las sumas son diferentes: puede avanzar en una columna, en la otra, o en ambas si es legal.
  - Si las sumas son iguales (x,x): avanzar 2 pasos en esa columna (equivalente a mover dos veces esa suma).

## Runners/Marcadores temporales
- Máximo 3 columnas activas por turno.
- "Columna activa" significa que tiene progreso temporal en este turno.
- Se puede avanzar en columnas ya activas sin límite.
- Para avanzar en una columna nueva (no activa), solo si aún hay <3 activas.

## Legalidad de movimientos
Un movimiento que avanza una columna es legal si:
- La columna NO está ya completada por el jugador.
- Si la columna no está activa, todavía hay menos de 3 columnas activas.
- Además, el total (permanente + temporal) no excede la altura (al exceder, se considera completada exactamente al alcanzar altura; no permitir overflow silencioso, debe capear o impedir).

## Bust ("se pasó")
Si en una tirada NO existe ningún movimiento legal posible (considerando las 3 particiones y las opciones de mover una o dos columnas), entonces:
- Se pierde TODO el progreso temporal del turno (se descarta).
- El turno termina y pasa al siguiente jugador.

## Stop/Bank
En cualquier momento después de aplicar un movimiento legal, el bot puede decidir "parar":
- Todo el progreso temporal se convierte en permanente.
- Se actualizan columnas completadas (si permanente alcanza altura).
- El turno termina y pasa al siguiente jugador.

## Ganar
Un jugador gana inmediatamente cuando, tras bank, tiene 3 columnas completadas.

## Determinismo
- El simulador debe permitir `seed` para reproducibilidad.
- Ideal: inyectar RNG (random.Random) en vez de usar random global.

## Métricas (para runner)
- win_counts por bot/estrategia.
- bust_rate por jugador.
- promedio de tiradas por turno.
- promedio de progreso bancado por turno (pasos bancados).
- duración en turnos por partida.
