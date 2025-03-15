from fractaltext.item import ElemDict, ElemList, ItemDict, ItemList
from fractaltext.proofwrite import (
  delete_naked,
  exists_naked,
  insert_naked,
  itself,
  lookup,
  update_naked,
)


class TestProofwrite:
  def test_delete(self):
    item = ItemList([ElemList(False, "test")])
    path = itself()
    assert delete_naked(item, path, 0) == ItemList([])

  def test_insert(self):
    item = ItemList([ElemList(False, "test")])
    path = itself()
    assert insert_naked(item, path, 0, "value") == ItemList(
      [ElemList(False, "value"), ElemList(False, "test")]
    )
    assert insert_naked(item, path, 2, "value") == ItemList(
      [ElemList(False, "value"), ElemList(False, "test"), ElemList(False, "value")]
    )

  def test_update(self):
    item = ItemList([ElemList(False, "test")])
    path = itself()
    assert update_naked(item, path, 0, "value") == ItemList([ElemList(False, "value")])

  def test_lookup(self):
    item = ItemDict(
      [
        ElemDict("key1", ItemList([])),
        ElemDict("key2", ItemList([ElemList(False, "unreachable")])),
      ]
    )
    item2 = ItemDict(
      [
        ElemDict("key1", ItemList([ElemList(False, "value1")])),
        ElemDict("key2", ItemList([ElemList(False, "unreachable")])),
      ]
    )
    path = lookup("key1", itself())
    assert insert_naked(item, path, 0, "value1") == item2

  def test_exists(self):
    item = ItemDict([ElemDict("key", ItemList([ElemList(False, "value")]))])
    assert exists_naked(item, lookup("key", itself()))
    assert not exists_naked(item, itself())
    assert not exists_naked(item, lookup("key", lookup("key2", itself())))
    assert not exists_naked(item, lookup("different", itself()))
