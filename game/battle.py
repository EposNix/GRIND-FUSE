"""Simple 3v3 lane battle simulator with light trait synergies."""

from dataclasses import dataclass, field
from typing import Dict, List

from .card import Card

# Basic synergy rules inspired by the design overview. Each entry maps a trait
# to the minimum count required on a team and the bonus it grants when active.
# Bonuses are intentionally lightweight to keep the simulation fast and
# deterministic.
SYNERGY_RULES: Dict[str, Dict[str, float]] = {
    # Two oozes regenerate 1 HP at the end of each round.
    "ooze": {"count": 2, "regen": 1},
    # Two knights gain +1 attack.
    "knight": {"count": 2, "atk_bonus": 1},
}


@dataclass
class Unit:
    card: Card
    hp: float
    atk_bonus: float = 0.0
    regen: float = 0.0
    max_hp: float = field(init=False)

    def __post_init__(self) -> None:
        # Track max HP so regeneration does not exceed the starting value.
        self.max_hp = self.hp

    @property
    def atk(self) -> float:
        return self.card.stats.get("atk", 0) + self.atk_bonus

    @property
    def spd(self) -> float:
        return self.card.stats.get("spd", 1.0)

    def alive(self) -> bool:
        return self.hp > 0


def _is_team_alive(team: List[Unit]) -> bool:
    return any(u.alive() for u in team)


def _apply_synergies(team: List[Unit]) -> None:
    """Apply trait-based bonuses to a team of units."""
    trait_counts: Dict[str, int] = {}
    for unit in team:
        for trait in unit.card.traits:
            trait_counts[trait] = trait_counts.get(trait, 0) + 1
    for trait, count in trait_counts.items():
        rule = SYNERGY_RULES.get(trait)
        if rule and count >= rule.get("count", 0):
            for unit in team:
                if trait in unit.card.traits:
                    unit.atk_bonus += rule.get("atk_bonus", 0)
                    unit.regen += rule.get("regen", 0)

def simulate_battle(team_a_cards: List[Card], team_b_cards: List[Card]) -> str:
    """Run a deterministic battle returning "A" or "B" winner.

    Each team supplies up to three cards. Units attack the opposing lane; if their
    lane target is down they attack the first remaining enemy. Speed determines
    action order each round. No abilities are currently modeled.
    """
    team_a = [Unit(c, c.stats.get("hp", 1)) for c in team_a_cards]
    team_b = [Unit(c, c.stats.get("hp", 1)) for c in team_b_cards]

    # pad to 3 lanes for simplicity
    while len(team_a) < 3:
        team_a.append(Unit(Card(id="dummy", display_name="", set="", rank="E", rarity="Common", role="", stats={"atk":0,"hp":0,"spd":1.0}, ability={}), 0))
    while len(team_b) < 3:
        team_b.append(Unit(Card(id="dummy", display_name="", set="", rank="E", rarity="Common", role="", stats={"atk":0,"hp":0,"spd":1.0}, ability={}), 0))

    # apply synergies after teams are assembled
    _apply_synergies(team_a)
    _apply_synergies(team_b)

    while _is_team_alive(team_a) and _is_team_alive(team_b):
        order = []
        for side, team in (("A", team_a), ("B", team_b)):
            for idx, unit in enumerate(team):
                if unit.alive():
                    order.append((unit.spd, side, idx))
        # higher speed acts first; tie breaks with team A
        order.sort(key=lambda t: (-t[0], t[1]))

        for _, side, idx in order:
            attacker = team_a[idx] if side == "A" else team_b[idx]
            if not attacker.alive():
                continue
            targets = team_b if side == "A" else team_a
            target = targets[idx]
            if not target.alive():
                # pick first alive
                target = next((u for u in targets if u.alive()), None)
            if target is None:
                return side
            target.hp -= attacker.atk
        # apply end-of-round regeneration
        for unit in team_a + team_b:
            if unit.alive() and unit.regen:
                unit.hp = min(unit.max_hp, unit.hp + unit.regen)
        # loop until one team dead
    return "A" if _is_team_alive(team_a) else "B"
