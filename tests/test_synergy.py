from game.card import Card
from game.battle import simulate_battle

def make_card(id_suffix: str, traits=None):
    return Card(
        id=f"test_{id_suffix}_E",
        display_name="",
        set="",
        rank="E",
        rarity="Common",
        role="",
        stats={"atk":1, "hp":3, "spd":1.0},
        ability={},
        traits=traits or [],
        art_tags=[],
        flavor="",
    )

def test_ooze_synergy_regenerates():
    ooze = make_card("ooze", traits=["ooze"])
    generic = make_card("generic")
    winner = simulate_battle([ooze, ooze], [generic, generic])
    assert winner == "A"

def test_knight_synergy_attack_bonus():
    knight = make_card("knight", traits=["knight"])
    generic = make_card("generic")
    winner = simulate_battle([knight, knight], [generic, generic])
    assert winner == "A"
