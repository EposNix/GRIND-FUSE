# GRIND//FUSE

Prototype skeleton for the GRIND//FUSE auto‑battler. This repository starts the codebase with
sample content, core models, and pack opening + fusion logic.

## Project Structure

```
Content/
  Cards/        # sample card JSON
  Packs/        # pack odds + pity thresholds

game/           # Python modules implementing ranks, cards, and pack opening

tests/          # unit tests covering fusion, pity, and combat synergies
```

## Quickstart

1. Ensure Python 3.10+ is installed.
2. Install development dependencies (pytest only):
   ```bash
   pip install pytest
   ```
3. Run tests:
   ```bash
   pytest
   ```

4. Run the tiny demonstration:
   ```bash
   python demo.py
   ```

These basics demonstrate the core 10→1 fusion mechanic and pack pity system.
