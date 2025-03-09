from fractaltext.item import ElemList, ElemDict, Item, ItemList, ItemDict
from fractaltext.serialize import dump_naked

from io import StringIO
import os
import pytest
from typing import Any


def serialize_all(it: Item, isucc: int = 2) -> str:
    with StringIO() as f:
      dump_naked(it, f, isucc)
      return f.getvalue()

class TestSerializer:
  def test_serialize_example(self):
    item = ItemDict([
      ElemDict('key1', ItemList([ElemList(False, 'child1'), ElemList(True, 'child2')])),
      ElemDict('key2', ItemList([])),
      ElemDict('key3', ItemList([ElemList(True, ''), ElemList(False, 'child3')])),
      ])
    serialized = serialize_all(item)
    assert serialized == """\
:key1
  child1
  "child2"
:key2
:key3
  ""
  child3
"""
