from fractaltext.proofwrite import itself, lookup, exists_naked, delete_naked, insert_naked, update_naked
from fractaltext.item import ElemList, ElemDict, Item, ItemList, ItemDict

class TestProofwrite:
  def test_delete(self):
    item = ItemList(['test'])
    path = itself()
    assert delete_naked(item, path, 0) == ItemList([])
  def test_insert(self):
    item = ItemList(['test'])
    path = itself()
    assert insert_naked(item, path, 0, 'value') == ItemList(['value', 'test'])
    assert insert_naked(item, path, 1, 'value') == ItemList(['test', 'value'])
  def test_update(self):
    item = ItemList(['test'])
    path = itself()
    assert update_naked(item, path, 0, 'value') == ItemList(['value'])
  def test_lookup(self):
    item = ItemDict([ElemDict('key1', ItemList([])), ElemDict('key2', ItemList(['unreachable']))])
    item2 = ItemDict([ElemDict('key1', ItemList(['value1'])), ElemDict('key2', ItemList(['unreachable']))])
    path = lookup('key1', itself())
    assert insert_naked(item, path, 0, 'value1') == item2
  def test_exists(self):
    item = ItemDict([ElemDict('key', ItemList(['value']))])
    assert exists_naked(item, lookup('key', itself()))
    assert not exists_naked(item, itself())
    assert not exists_naked(item, lookup('key', lookup('key2', itself())))
    assert not exists_naked(item, lookup('different', itself()))
