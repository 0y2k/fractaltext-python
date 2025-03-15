import json
import os
from typing import Any

import pytest

from fractaltext.item import ElemDict, ElemList, Item, ItemDict, ItemList, should_quote
from fractaltext.parse import FractalTextParseError, load_naked, parse_naked

dir_path: str = "./vendor/github.com/0y2k/fractaltext-test"
load_path: str = os.path.join(dir_path, "load")


def generate_load_names():
  return [d for d in os.listdir(load_path) if os.path.isdir(os.path.join(load_path, d))]


def item_from_object(obj: Any) -> Item:
  if isinstance(obj, list):
    rs = []
    for x in obj:
      rs.append(ElemList(should_quote(x), x))
    return ItemList(rs)
  elif isinstance(obj, dict):
    rs = []
    for k, v in obj.items():
      rs.append(ElemDict(k, item_from_object(v)))
    return ItemDict(rs)
  else:
    raise ValueError


class TestParser:
  @pytest.mark.parametrize("name", generate_load_names())
  def test_load(self, name):
    case_path = os.path.join(load_path, name)
    load_in_path = os.path.join(case_path, "load_in.ft")
    load_out_path = os.path.join(case_path, "load_out.json")
    load_err_path = os.path.join(case_path, "load_err.json")
    if os.path.exists(load_out_path):
      with open(load_out_path, encoding="utf-8") as f:
        expected = item_from_object(json.load(f))
      with open(load_in_path, encoding="utf-8") as f:
        result = load_naked(f)
      assert result == expected, (
        f"Got different result. expected: {expected}, got: {result}"
      )
    elif os.path.exists(load_err_path):
      with open(load_err_path, encoding="utf-8") as f:
        expected_err = json.load(f)
      with pytest.raises(FractalTextParseError) as err:
        with open(load_in_path, encoding="utf-8") as f:
          load_naked(f)
      assert err.value.line_no == expected_err["line"], (
        f"Got an error in different location. expected: {expected_err['line']}, got: {err.value.line_no}"
      )
    else:
      raise RuntimeError("No expected result")

  def test_parse_example(self):
    sample_text = """
# This is a comment
:key1
  child1
  "child2"

:key2
  # Child block is empty here

:key3
  ""
  child3
"""
    parsed = parse_naked(sample_text)
    assert parsed == ItemDict(
      [
        ElemDict(
          "key1", ItemList([ElemList(False, "child1"), ElemList(True, "child2")])
        ),
        ElemDict("key2", ItemList([])),
        ElemDict("key3", ItemList([ElemList(True, ""), ElemList(False, "child3")])),
      ]
    )
