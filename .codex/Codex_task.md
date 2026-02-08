# Objetivo
Generar un simulador del juego "Can't Stop" (reglas clásicas) para 4 jugadores con bots automáticos y un runner de experimentos. Debe ser determinista con seed. Debe incluir pruebas unitarias, incluyendo una prueba que corra X repeticiones (parámetro configurable) y valide métricas con tolerancias.

# Reglas
Ver SPEC.md (obligatorio seguirlo).

# Bots
Ver BOTS.md (obligatorio implementar exactamente esas políticas).

# Testing
Ver TESTING.md (obligatorio: tests deterministas, y test repetitivo con X).

# Tareas (en orden)
1. Crear motor del juego (estado, turnos, tiradas, legal_moves, apply_move, bust, bank, win condition).
2. Crear interfaz de bot + bots: AlwaysContinue, MaxNRolls(N), GreedyAggressive, GreedyConservative, RiskStop(T) (opcional si se define en BOTS).
3. Crear runner de simulación para N partidas con seed inicial y reporte de métricas.
4. Crear suite de tests:
   - tests de reglas (pairings, legal_moves, bust, bank, win condition).
   - tests deterministas de partida completa con seed fijo.
   - test estadístico repetitivo: corre X partidas y verifica rangos/tolerancias.
5. Documentar cómo ejecutar: `python -m ...` o similar, y cómo cambiar X repeticiones/seed.

# Restricciones
- No crear UI.
- Enfocarse en claridad y testabilidad.
- No usar librerías externas salvo estándar (random, dataclasses, typing, unittest/pytest).
