from abc import ABC
from copy import deepcopy
from typing import Literal

from .item import DocumentA, Item, ItemList


class FractalTextEditError(Exception):
  def __init__(self, message: str):
    super().__init__(message)


class Path(ABC):
  kind: Literal["itself", "lookup"]


class PathItself(Path):
  kind: Literal["itself"]

  def __init__(self):
    self.kind = "itself"


class PathLookup(Path):
  kind: Literal["lookup"]
  key: str
  next_path: Path

  def __init__(self, k: str, n: Path):
    self.kind = "lookup"
    self.key = k
    self.next_path = n


def itself() -> Path:
  return PathItself()


def lookup(k: str, n: Path) -> Path:
  return PathLookup(k, n)


class Edit(ABC):
  kind: Literal["delete", "insert", "update"]


class EditDelete(Edit):
  kind: Literal["delete"]
  index: int

  def __init__(self, i: int):
    self.kind = "delete"
    self.index = i


class EditInsert(Edit):
  kind: Literal["insert"]
  index: int
  value: str

  def __init__(self, i: int, v: str):
    self.kind = "insert"
    self.index = i
    self.value = v


class EditUpdate(Edit):
  kind: Literal["update"]
  index: int
  value: str

  def __init__(self, i: int, v: str):
    self.kind = "update"
    self.index = i
    self.value = v


def apply(it0: ItemList, e: Edit) -> ItemList:
  it = deepcopy(it0)
  if it0.kind != "list":
    raise FractalTextEditError("Expected list, got dict")
  n = len(it.entries)
  if e.kind == "delete":
    if 0 <= e.index < n:
      del it.entries[e.index]
    else:
      raise IndexError
  elif e.kind == "insert":
    if 0 <= e.index <= n:
      els = it.entries
      it.entries = els[0 : e.index] + [e.value] + els[e.index :]
    else:
      raise IndexError
  elif e.kind == "update":
    if 0 <= e.index < n:
      it.entries[e.index] = e.value
    else:
      raise IndexError
  return it


def edit(it0: Item, p: Path, e: Edit) -> Item:
  if p.kind == "itself":
    if it0.kind == "list":
      try:
        return apply(it0, e)
      except IndexError:
        raise FractalTextEditError("Index is out of bound")
      except Exception as ex:
        raise ex
    else:
      raise FractalTextEditError("Expected list, got dict")
  elif p.kind == "lookup":
    if it0.kind == "dict":
      j = next((i for (i, ed) in enumerate(it0.entries) if ed.key == p.key), None)
      if j is None:
        raise FractalTextEditError(f"No such key: {p.key}")
      it = deepcopy(it0)
      it.entries[j].value = edit(it.entries[j].value, p.next_path, e)
      return it
    else:
      raise FractalTextEditError("Expected dict, got list")
  else:
    raise ValueError


def delete(doc0: DocumentA, p: Path, i: int) -> DocumentA:
  doc = deepcopy(doc0)
  doc.item = edit(doc.item, p, EditDelete(i))
  return doc


def insert(doc0: DocumentA, p: Path, i: int, v: str) -> DocumentA:
  doc = deepcopy(doc0)
  doc.item = edit(doc.item, p, EditInsert(i, v))
  return doc


def update(doc0: DocumentA, p: Path, i: int, v: str) -> DocumentA:
  doc = deepcopy(doc0)
  doc.item = edit(doc.item, p, EditUpdate(i, v))
  return doc


def delete_naked(it: Item, p: Path, i: int) -> Item:
  return edit(it, p, EditDelete(i))


def insert_naked(it: Item, p: Path, i: int, v: str) -> Item:
  return edit(it, p, EditInsert(i, v))


def update_naked(it: Item, p: Path, i: int, v: str) -> Item:
  return edit(it, p, EditUpdate(i, v))


def exists_naked(it: Item, p: Path) -> bool:
  if p.kind == "itself":
    if it.kind == "list":
      return True
    else:
      return False
  elif p.kind == "lookup":
    if it.kind == "dict":
      ed = next((ed for ed in it.entries if ed.key == p.key), None)
      if ed is None:
        return False
      else:
        return exists_naked(ed.value, p.next_path)
    else:
      return False
  else:
    raise ValueError


def exists(doc: DocumentA, p: Path) -> bool:
  return exists_naked(doc.item, p)
