"""Pack opening with pity counters and duplicate protection."""

import json
import random
from pathlib import Path
from typing import Dict, List, Optional

from . import ranks

RARITY_ORDER = ["Common", "Uncommon", "Rare", "Mythic"]


class PackOpener:
    def __init__(self, rarity_odds: Dict[str, float], pity: Dict[str, int], cards_per_pack: int = 5, rng: Optional[random.Random] = None):
        self.rarity_odds = rarity_odds
        self.pity = pity
        self.cards_per_pack = cards_per_pack
        self.rng = rng or random.Random()
        self.packs_since = {"Rare": 0, "Mythic": 0}

    def _roll_rarity(self) -> str:
        r = self.rng.random()
        cumulative = 0.0
        for rarity in RARITY_ORDER:
            cumulative += self.rarity_odds.get(rarity, 0)
            if r < cumulative:
                return rarity
        return RARITY_ORDER[0]

    def open_pack(self) -> List[str]:
        rarities = [self._roll_rarity() for _ in range(self.cards_per_pack)]
        # Apply pity for Mythic then Rare
        for rarity in ["Mythic", "Rare"]:
            threshold = self.pity.get(f"{rarity.lower()}_at")
            if threshold is None:
                continue
            if self.packs_since[rarity] + 1 >= threshold and rarity not in rarities:
                rarities[-1] = rarity
        # update counters
        highest = max(rarities, key=RARITY_ORDER.index)
        for rarity in ["Rare", "Mythic"]:
            if RARITY_ORDER.index(highest) >= RARITY_ORDER.index(rarity):
                self.packs_since[rarity] = 0
            else:
                self.packs_since[rarity] += 1
        return rarities


class CardPackOpener(PackOpener):
    """Pack opener that returns actual cards using a card library.

    If a ``collection`` is supplied, the opener will attempt to avoid granting an
    11th copy of a card by filtering out cards for which the collection already
    holds ``ranks.FUSION_COST`` copies. This implements the soft duplicate
    protection described in the design overview.
    """

    def __init__(
        self,
        library,
        rarity_odds: Dict[str, float],
        pity: Dict[str, int],
        cards_per_pack: int = 5,
        rng: Optional[random.Random] = None,
        collection=None,
    ):
        super().__init__(rarity_odds, pity, cards_per_pack, rng)
        self.library = library
        self.collection = collection

    def open_pack_cards(self):
        rarities = self.open_pack()
        cards = []
        for r in rarities:
            card = self.library.random_by_rarity(
                r,
                self.rng,
                predicate=(
                    None
                    if self.collection is None
                    else lambda c: self.collection.count(c.id) < ranks.FUSION_COST
                ),
            )
            cards.append(card)
            if self.collection is not None:
                self.collection.add(card)
        return cards


def load_card_pack(library, path: str, rng: Optional[random.Random] = None, collection=None) -> CardPackOpener:
    """Load pack configuration from JSON and return a ``CardPackOpener``."""
    data = json.loads(Path(path).read_text())
    return CardPackOpener(
        library,
        data.get("rarity_odds", {}),
        data.get("pity", {}),
        cards_per_pack=data.get("cards_per_pack", 5),
        rng=rng,
        collection=collection,
    )
