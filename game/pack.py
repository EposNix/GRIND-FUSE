"""Pack opening with pity counters."""

import random
from typing import Dict, List, Optional

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
