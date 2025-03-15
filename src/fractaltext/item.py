from abc import ABC, abstractmethod
from typing import Any, Literal


class Token(ABC):
  kind: Literal["blank", "comment", "key", "value"]


class TokenSurplus(Token):
  kind: Literal["blank", "comment"]


class TokenValid(Token):
  kind: Literal["key", "value"]
  indent: int

  def __init__(self, i: int):
    self.indent = i


class TokenBlank(TokenSurplus):
  kind: Literal["blank"]

  def __init__(self):
    self.kind = "blank"


class TokenComment(TokenSurplus):
  kind: Literal["comment"]
  indent: int
  content: str

  def __init__(self, i: int, c: str):
    self.kind = "comment"
    self.indent = i
    self.content = c


class TokenKey(TokenValid):
  kind: Literal["key"]
  content: str

  def __init__(self, i: int, c: str):
    super().__init__(i)
    self.kind = "key"
    self.content = c


class TokenValue(TokenValid):
  kind: Literal["value"]
  quoted: bool
  content: str

  def __init__(self, i: int, q: bool, c: str):
    super().__init__(i)
    self.kind = "value"
    self.quoted = q
    self.content = c


class Item(ABC):
  kind: Literal["list", "dict"]
  annotated: bool

  def __init__(self):
    self.annotated = False

  @abstractmethod
  def __eq__(self, obj: Any):
    return NotImplemented


class ElemList:
  quoted: bool
  content: str

  def __init__(self, q: bool, c: str):
    self.quoted = q
    self.content = c

  def __eq__(self, obj: Any):
    if not isinstance(obj, ElemList):
      return NotImplemented
    return self.content == obj.content


class ElemDict:
  key: str
  value: Item

  def __init__(self, k: str, v: Item):
    self.key = k
    self.value = v

  def __eq__(self, obj: Any):
    if not isinstance(obj, ElemDict):
      return NotImplemented
    return self.key == obj.key and self.value == obj.value


class ItemList(Item):
  kind: Literal["list"]
  entries: list[ElemList]

  def __init__(self, entries: list[ElemList], **kwargs):
    self.kind = "list"
    super().__init__(**kwargs)
    self.entries = entries

  def __eq__(self, obj: Any):
    if not isinstance(obj, Item):
      return NotImplemented
    if obj.kind == "list":
      return self.entries == obj.entries
    return False


class ItemDict(Item):
  kind: Literal["dict"]
  entries: list[ElemDict]

  def __init__(self, entries: list[ElemDict], **kwargs):
    self.kind = "dict"
    super().__init__(**kwargs)
    if len(entries) == 0:
      raise ValueError
    self.entries = entries

  def __eq__(self, obj: Any):
    if not isinstance(obj, Item):
      return NotImplemented
    if obj.kind == "dict":
      return self.entries == obj.entries
    return False


class ItemA(Item):
  indent: int

  def __init__(self, indent: int, **kwargs):
    super().__init__(**kwargs)
    self.indent = indent
    self.annotated = True


class ElemAList:
  surplus_tokens: list[TokenSurplus]
  quoted: bool
  content: str

  def __init__(self, st: list[TokenSurplus], q: bool, c: str):
    self.surplus_tokens = st
    self.quoted = q
    self.content = c

  def __eq__(self, obj: Any):
    if not isinstance(obj, ElemList):
      return NotImplemented
    return self.content == obj.content


class ElemADict:
  surplus_tokens: list[TokenSurplus]
  key: str
  value: ItemA

  def __init__(self, st: list[TokenSurplus], k: str, v: ItemA):
    self.surplus_tokens = st
    self.key = k
    self.value = v

  def __eq__(self, obj: Any):
    if not isinstance(obj, ElemDict):
      return NotImplemented
    return self.key == obj.key and self.value == obj.value


class ItemAList(ItemA, ItemList):
  kind: Literal["list"]

  def __init__(self, indent: int, entries: list[ElemAList]):
    self.kind = "list"
    super().__init__(indent=indent, entries=entries)


class ItemADict(ItemA, ItemDict):
  kind: Literal["dict"]

  def __init__(self, indent: int, entries: list[ElemADict]):
    self.kind = "dict"
    super().__init__(indent=indent, entries=entries)


class DocumentA:
  item: ItemA
  surplus_tokens: list[TokenSurplus]

  def __init__(self, it: ItemA, sts: list[TokenSurplus]):
    self.item = it
    self.surplus_tokens = sts


def should_quote(s: str) -> bool:
  if len(s) == 0:
    return True
  if s[0] in [" ", "\t", "#", ":"]:
    return True
  if s[0] == '"' and s[-1] == '"':
    return True
  return False
