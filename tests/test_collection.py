from game.collection import Collection
from game.library import CardLibrary


def test_collection_fuses_when_enough_copies():
    library = CardLibrary("Content/Cards")
    base = library.get("slime_knight_001_E")
    coll = Collection()
    for _ in range(10):
        coll.add(base)
    assert coll.can_fuse(base.id)
    fused = coll.fuse_card(base)
    assert fused.rank == "F"
    assert coll.count(base.id) == 0
    assert coll.count(fused.id) == 1
