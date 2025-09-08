import json
from pathlib import Path

from game.card import Card
from game.battle import simulate_battle


def load_card():
    data = json.loads(Path("Content/Cards/sample_slime_knight_E.json").read_text())
    return Card(**data)


def test_stronger_team_wins():
    weak = load_card()
    strong_data = json.loads(Path("Content/Cards/sample_slime_knight_E.json").read_text())
    strong_data["stats"]["atk"] *= 2
    strong_data["stats"]["hp"] *= 2
    strong = Card(**strong_data)

    winner = simulate_battle([strong]*3, [weak]*3)
    assert winner == "A"
