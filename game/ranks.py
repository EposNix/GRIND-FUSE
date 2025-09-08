"""Rank model utilities."""

RANKS = ["E", "F", "D", "C", "B", "A", "S", "SS", "SSS"]
FUSION_COST = 10
POWER_BASE = 1

rank_to_index = {r: i for i, r in enumerate(RANKS)}


def power(base_power: int, rank: str) -> int:
    """Return power scaled by rank using the 10x gospel."""
    return int(base_power * (10 ** rank_to_index[rank]))


def next_rank(rank: str) -> str:
    idx = rank_to_index[rank]
    if idx + 1 >= len(RANKS):
        raise ValueError("Cannot fuse beyond highest rank")
    return RANKS[idx + 1]
