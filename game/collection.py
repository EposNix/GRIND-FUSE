"""Manage a player's card collection and handle fusions."""

from collections import defaultdict
from typing import Dict

from .card import Card, fuse
from . import ranks


class Collection:
    def __init__(self):
        self.counts: Dict[str, int] = defaultdict(int)

    def add(self, card: Card, count: int = 1) -> None:
        self.counts[card.id] += count

    def count(self, card_id: str) -> int:
        return self.counts.get(card_id, 0)

    def can_fuse(self, card_id: str) -> bool:
        return self.count(card_id) >= ranks.FUSION_COST

    def fuse_card(self, card: Card) -> Card:
        if not self.can_fuse(card.id):
            raise ValueError("Insufficient copies to fuse")
        self.counts[card.id] -= ranks.FUSION_COST
        fused = fuse([card] * ranks.FUSION_COST)
        self.counts[fused.id] += 1
        return fused
