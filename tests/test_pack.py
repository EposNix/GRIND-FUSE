from game.pack import PackOpener
import random


def test_rare_pity_triggers_on_tenth_pack():
    odds = {"Common": 1.0}
    pity = {"rare_at": 10, "mythic_at": 30}
    opener = PackOpener(odds, pity, rng=random.Random(0))
    for _ in range(9):
        rarities = opener.open_pack()
        assert all(r == "Common" for r in rarities)
    tenth = opener.open_pack()
    assert "Rare" in tenth
    assert opener.packs_since["Rare"] == 0
