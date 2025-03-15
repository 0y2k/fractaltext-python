from collections.abc import Iterable
from typing import TextIO

from .item import DocumentA, Item, ItemA, TokenSurplus


def render_surplus_tokens(tss: list[TokenSurplus]) -> Iterable[str]:
  for ts in tss:
    if ts.kind == "blank":
      yield "\n"
    elif ts.kind == "comment":
      yield " " * ts.indent + "#" + ts.content + "\n"
    else:
      raise ValueError


def serialize(doc: DocumentA) -> Iterable[str]:
  """serialize

  Convert annotated document into text stream.

  Args:
    doc (DocumentA): input annotated document

  Returns:
    Iterable[str]: output linewise text stream
  """

  def pt(it: ItemA) -> Iterable[str]:
    if it.kind == "list":
      for el in it.entries:
        yield from render_surplus_tokens(el.surplus_tokens)
        r = '"' + el.content + '"' if el.quoted else el.content
        yield " " * it.indent + r + "\n"
    elif it.kind == "dict":
      for ed in it.entries:
        yield from render_surplus_tokens(ed.surplus_tokens)
        yield " " * it.indent + ":" + ed.key + "\n"
        yield from pt(ed.value)
    else:
      raise ValueError

  yield from pt(doc.item)
  yield from render_surplus_tokens(doc.surplus_tokens)


def serialize_naked(it0: Item, isucc: int = 2) -> Iterable[str]:
  """serialize_naked

  Convert naked document into text stream.

  Args:
    doc (DocumentA): input naked document
    isucc (int): indent width

  Returns:
    Iterable[str]: output linewise text stream
  """
  if it0.annotated:
    serialize(DocumentA(it0, []))

  def pt(i: int, it: Item) -> Iterable[str]:
    if it.kind == "list":
      for el in it.entries:
        r = '"' + el.content + '"' if el.quoted else el.content
        yield " " * i + r + "\n"
    elif it.kind == "dict":
      for ed in it.entries:
        yield " " * i + ":" + ed.key + "\n"
        yield from pt(i + isucc, ed.value)
    else:
      raise ValueError

  return pt(0, it0)


def dump(doc: DocumentA, f: TextIO):
  """dump

  Write serialized document which is annotated.

  Args:
    doc (DocumentA): input annotated document
    f (TextIO): output text stream
  """
  for line in serialize(doc):
    f.write(line)


def dump_naked(it: Item, f: TextIO, isucc: int = 2):
  """dump_naked

  Write serialized document which is naked.

  Args:
    doc (DocumentA): input naked document
    f (TextIO): output text stream
    isucc (int): indent width
  """
  for line in serialize_naked(it, isucc):
    f.write(line)
