"""Card model and fusion helpers."""

from dataclasses import dataclass, field
from typing import List, Dict

from . import ranks


@dataclass
class Card:
    id: str
    display_name: str
    set: str
    rank: str
    rarity: str
    role: str
    stats: Dict[str, float]
    ability: Dict[str, str]
    traits: List[str] = field(default_factory=list)
    art_tags: List[str] = field(default_factory=list)
    flavor: str = ""

    def power(self) -> int:
        return ranks.power(self.stats.get("atk", ranks.POWER_BASE), self.rank)


def fuse(cards: List[Card]) -> Card:
    """Fuse cards of the same id and rank into the next rank."""
    if len(cards) != ranks.FUSION_COST:
        raise ValueError("Need exactly 10 cards to fuse")
    first = cards[0]
    if any(c.id != first.id or c.rank != first.rank for c in cards):
        raise ValueError("Cards must share id and rank")
    fused_rank = ranks.next_rank(first.rank)
    fused_stats = {k: v * 10 for k, v in first.stats.items()}
    fused_id = f"{first.id[:-2]}_{fused_rank}" if first.id.endswith(f"_{first.rank}") else f"{first.id}_{fused_rank}"
    return Card(
        id=fused_id,
        display_name=first.display_name,
        set=first.set,
        rank=fused_rank,
        rarity=first.rarity,
        role=first.role,
        stats=fused_stats,
        ability=first.ability,
        traits=first.traits,
        art_tags=first.art_tags,
        flavor=first.flavor,
    )
