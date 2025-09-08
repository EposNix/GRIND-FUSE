"""Run a tiny demonstration of pack opening, fusion, and battle."""

import json
from pathlib import Path
from game.card import Card, fuse
from game.pack import PackOpener
from game.battle import simulate_battle


def main():
    data = json.loads(Path("Content/Cards/sample_slime_knight_E.json").read_text())
    base = Card(**data)
    cards = [base for _ in range(10)]
    fused = fuse(cards)
    print(f"Fused into {fused.id} with atk={fused.stats['atk']}")

    odds = {"Common": 0.9, "Uncommon": 0.1}
    pity = {"rare_at": 10, "mythic_at": 30}
    opener = PackOpener(odds, pity)
    rarities = opener.open_pack()
    print(f"Opened pack rarities: {rarities}")

    winner = simulate_battle([fused]*3, [base]*3)
    print(f"Battle winner: Team {winner}")


if __name__ == "__main__":
    main()
