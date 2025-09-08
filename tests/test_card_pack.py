import random

from game.collection import Collection
from game.library import CardLibrary
from game.pack import CardPackOpener


def test_open_pack_returns_cards():
    library = CardLibrary("Content/Cards")
    odds = {"Common": 1.0}
    pity = {}
    opener = CardPackOpener(library, odds, pity, rng=random.Random(0))
    cards = opener.open_pack_cards()
    assert len(cards) == opener.cards_per_pack
    assert all(c.rarity == "Common" for c in cards)


def test_duplicate_protection_skips_eleventh_copy():
    library = CardLibrary("Content/Cards")
    coll = Collection()
    blocked = library.get("pebble_imp_001_E")
    coll.add(blocked, 10)
    odds = {"Common": 1.0}
    pity = {}
    opener = CardPackOpener(library, odds, pity, rng=random.Random(0), collection=coll)
    cards = opener.open_pack_cards()
    assert all(c.id != blocked.id for c in cards)
