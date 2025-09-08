"""Run a tiny demonstration of pack opening, collection fusion, and battle."""

from game.battle import simulate_battle
from game.collection import Collection
from game.library import CardLibrary
from game.pack import load_card_pack


def main():
    library = CardLibrary("Content/Cards")
    collection = Collection()

    base = library.get("slime_knight_001_E")
    for _ in range(10):
        collection.add(base)
    fused = collection.fuse_card(base)
    print(f"Fused into {fused.id} with atk={fused.stats['atk']}")

    # Preload another card to demonstrate duplicate protection during pack opening.
    pebble = library.get("pebble_imp_001_E")
    collection.add(pebble, 10)

    opener = load_card_pack(library, "Content/Packs/core_pack.json", collection=collection)
    cards = opener.open_pack_cards()
    print("Opened pack: " + ", ".join(c.display_name for c in cards))

    winner = simulate_battle([fused] * 3, [base] * 3)
    print(f"Battle winner: Team {winner}")


if __name__ == "__main__":
    main()
