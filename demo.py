"""Run a tiny demonstration of pack opening, collection fusion, and battle."""

from game.battle import simulate_battle
from game.collection import Collection
from game.library import CardLibrary
from game.pack import CardPackOpener


def main():
    library = CardLibrary("Content/Cards")
    collection = Collection()

    base = library.get("slime_knight_001_E")
    for _ in range(10):
        collection.add(base)
    fused = collection.fuse_card(base)
    print(f"Fused into {fused.id} with atk={fused.stats['atk']}")

    odds = {"Common": 0.9, "Uncommon": 0.1}
    pity = {"rare_at": 10, "mythic_at": 30}
    opener = CardPackOpener(library, odds, pity)
    cards = opener.open_pack_cards()
    print("Opened pack: " + ", ".join(c.display_name for c in cards))

    winner = simulate_battle([fused] * 3, [base] * 3)
    print(f"Battle winner: Team {winner}")


if __name__ == "__main__":
    main()
