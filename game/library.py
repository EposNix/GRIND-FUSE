"""Load and query card data from JSON files."""

import json
import random
from pathlib import Path
from typing import Dict, List

from .card import Card


class CardLibrary:
    """Simple in-memory index of all cards."""

    def __init__(self, cards_dir: str = "Content/Cards"):
        self.cards: Dict[str, Card] = {}
        self.by_rarity: Dict[str, List[Card]] = {}
        self._load(cards_dir)

    def _load(self, cards_dir: str) -> None:
        for path in Path(cards_dir).glob("*.json"):
            data = json.loads(path.read_text())
            card = Card(**data)
            self.cards[card.id] = card
            self.by_rarity.setdefault(card.rarity, []).append(card)

    def get(self, card_id: str) -> Card:
        return self.cards[card_id]

    def random_by_rarity(self, rarity: str, rng: random.Random | None = None) -> Card:
        rng = rng or random
        pool = self.by_rarity.get(rarity)
        if not pool:
            raise ValueError(f"No cards with rarity {rarity}")
        return rng.choice(pool)
