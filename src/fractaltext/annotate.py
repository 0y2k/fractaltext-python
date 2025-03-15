from typing import Any

from typing_extensions import assert_never

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
  """peel

  Remove annotation.

  Args:
    doc (DocumentA): input annotated document

  Returns:
    Item: output document
  """

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
    assert_never(it.kind)

  return pt(doc.item)


def annotate(it0: Item, isucc: int = 2) -> DocumentA:
  """annotate

  Add annotation.

  Args:
    it0 (Item): input document
    isucc (int, optional): indent width. default is 2.

  Returns:
    DocumentA: output annotated document
  """
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
    assert_never(it.kind)

  return DocumentA(pt(0, it0), [])


def from_dict_naked(d: Any) -> Item:
  """from_dict_naked

  Convert from str-in-list-in-dict structure to document.

  Args:
    d (Any): input str-in-list-in-dict structure

  Returns:
    Item: output item

  Raises:
    ValueError: if d is not str-in-list-in-dict structure
  """
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
  """from_dict

  Convert from str-in-list-in-dict structure to annotated document.

  Args:
    d (Any): input str-in-list-in-dict structure
    isucc (int, optional): indent width. default is 2.

  Returns:
    DocumentA: output annotated document

  Raises:
    ValueError: if d is not str-in-list-in-dict structure
  """
  item = from_dict_naked(d)
  return annotate(item, isucc)


def to_dict_naked(it: Item) -> Any:
  """to_dict_naked

  Convert from document to str-in-list-in-dict structure.

  Args:
    it (Item): input document

  Returns:
    Any: output str-in-list-in-dict structure
  """
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
  assert_never(it.kind)


def to_dict(doc: DocumentA) -> Any:
  """to_dict

  Convert from annotated document to str-in-list-in-dict structure.

  Args:
    doc (DocumentA): input annotated document

  Returns:
    Any: output str-in-list-in-dict structure
  """
  return to_dict_naked(peel(doc))
