"""Simple 3v3 lane battle simulator."""

from dataclasses import dataclass
from typing import List

from .card import Card


@dataclass
class Unit:
    card: Card
    hp: float

    @property
    def atk(self) -> float:
        return self.card.stats.get("atk", 0)

    @property
    def spd(self) -> float:
        return self.card.stats.get("spd", 1.0)

    def alive(self) -> bool:
        return self.hp > 0


def _is_team_alive(team: List[Unit]) -> bool:
    return any(u.alive() for u in team)


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
        # loop until one team dead
    return "A" if _is_team_alive(team_a) else "B"
