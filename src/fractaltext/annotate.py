from typing import Any

from .item import (
  DocumentA,
  ElemADict,
  ElemAList,
  ElemDict,
  ElemList,
  Item,
  ItemA,
  ItemAList,
  ItemDict,
  ItemList,
  should_quote,
)


def peel(doc: DocumentA) -> Item:
  def pt(it: ItemA) -> Item:
    if it.kind == "list":
      res = []
      for el in it.entries:
        res.append(ElemList(el.quoted, el.content))
      return ItemList(res)
    elif it.kind == "dict":
      res = []
      for ed in it.entries:
        res.append(ElemDict(ed.key, pt(ed.value)))
      return ItemDict(res)
    else:
      raise ValueError

  return pt(doc.item)


def annotate(it0: Item, isucc: int = 2) -> DocumentA:
  if it0.annotated:
    return DocumentA(it0, [])

  def pt(i: int, it: Item) -> ItemA:
    if it.kind == "list":
      res = []
      for el in it.entries:
        res.append(ElemAList([], el.quoted, el.content))
      return ItemAList(i, res)
    elif it.kind == "dict":
      res = []
      for ed in it.entries:
        res.append(ElemADict([], ed.key, pt(i + isucc, ed.value)))
      return ItemAList(i, res)
    else:
      raise ValueError

  return DocumentA(pt(0, it0), [])


def from_dict_naked(d: Any) -> Item:
  if isinstance(d, list):
    if all(isinstance(e, str) for e in d):
      res = []
      for e in d:
        res.append(ElemList(should_quote(e), e))
      return ItemList(res)
    else:
      raise ValueError
  elif isinstance(d, dict):
    res = []
    for k, v in d.items():
      item = from_dict_naked(v)
      res.append(ElemDict(k, item))
    return ItemDict(res)
  else:
    raise ValueError


def from_dict(d: Any, isucc: int = 2) -> DocumentA:
  item = from_dict_naked(d)
  return DocumentA(annotate(item, isucc), [])


def to_dict_naked(it: Item) -> Any:
  if it.kind == "list":
    res = []
    for el in it.entries:
      res.append(el.content)
    return res
  elif it.kind == "dict":
    res = {}
    for ed in it.entries:
      res[ed.key] = to_dict_naked(ed.value)
    return res
  else:
    raise ValueError


def to_dict(doc: DocumentA) -> Any:
  return to_dict_naked(peel(doc))
