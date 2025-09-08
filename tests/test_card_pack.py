import random

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
