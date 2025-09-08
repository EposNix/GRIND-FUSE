import json
from pathlib import Path

from game.card import Card, fuse


def load_sample_card():
    data = json.loads(Path("Content/Cards/sample_slime_knight_E.json").read_text())
    return Card(**data)


def test_fusion_promotes_rank_and_stats():
    base = load_sample_card()
    cards = [base for _ in range(10)]
    fused = fuse(cards)
    assert fused.rank == "F"
    assert fused.stats["atk"] == base.stats["atk"] * 10
    assert fused.id.endswith("_F")
