# JuegoCantStop

Simulador determinista del juego **Can't Stop** para 4 jugadores con bots automáticos, runner de experimentos y tests.

## Ejecutar simulaciones

```bash
python -m cantstop --games 200 --seed 12345
```

Parámetros:
- `--games`: cantidad de partidas.
- `--seed`: seed base; cada partida usa `seed+i`.

## Ejecutar tests

```bash
python -m unittest discover -s tests -v
```

Test repetitivo configurable con variable de entorno:

```bash
CANTSTOP_X_REPS=500 python -m unittest tests.test_simulation.TestSimulation.test_repetitive_metrics -v
```

## Estructura

- `cantstop/engine.py`: motor del juego y reglas.
- `cantstop/bots.py`: bots y políticas.
- `cantstop/runner.py`: batch de partidas y métricas.
- `tests/`: pruebas unitarias y de simulación.
