from .item import DocumentA, ElemList, ElemDict, ElemAList, ElemADict, Item, ItemList, ItemDict, ItemA, ItemAList, ItemADict, Token, TokenBlank, TokenComment, TokenKey, TokenValue
from .annotate import peel

from collections.abc import Iterable
from more_itertools import peekable
import re
from typing import Literal, TextIO


class FractalTextParseError(Exception):
  line_no: int
  def __init__(self, message: str, n: int):
    super().__init__(message)
    self.line_no = n

class LineToken:
  token: Token
  line_no: int
  def __init__(self, t: Token, l: int):
    self.token = t
    self.line_no = l


def tokenize(lines: Iterable[str]) -> Iterable[LineToken]:
  """
  Tokenize the input text into a list of tokens.
  If a tab character is found in the indentation, an error is raised.
  """
  for lineno, line in enumerate(lines, start=1):
    indent = 0
    for char in line:
      if char == ' ':
        indent += 1
      # Check for illegal tab characters in the indentation
      elif char == '\t':
        raise FractalTextParseError("Tab character found in indentation", lineno)
      else:
        break
    content = line[indent:]
    # Classify the line based on its content
    if content == '':
      tok = TokenBlank()
    elif content.startswith('#'):
      content = content[1:]
      tok = TokenComment(indent, content)
    elif content.startswith(':'):
      content = content[1:]
      tok = TokenKey(indent, content)
    else:
      quoted = False
      # Remove surrounding double quotes if present (applied only once).
      if len(content) >= 2 and content[0] == '"' and content[-1] == '"':
        quoted = True
        content = content[1:-1]
      tok = TokenValue(indent, quoted, content)
    yield LineToken(tok, lineno)


def parse_document(tokens: Iterable[LineToken]) -> DocumentA:
  """
  Recursively parse tokens starting at a given index and indentation level.
  Returns an Item.

  Parsing rules:
    - Only tokens with indent equal to current_indent are processed at this level.
    - Blank and comment tokens are ignored.
    - The mode is determined by the first non-blank/comment token:
      * If it is a value token, the block is parsed as a list (ItemList).
      * If it is a key token, the block is parsed as a dictionary (ItemDict).
    - Mixing key and value tokens at the same level is not allowed.
    - For each key token, its associated child block is defined by subsequent tokens with indent greater than current_indent.
      If no such tokens exist, the child item is set to ItemEmptyList.
  """
  discharge = []
  p = peekable(tokens)
  def parse_item(current_indent: int | None) -> Item:
    nonlocal discharge
    while True:
      n = p.peek(default = None)
      if n is None:
        return ItemList([])
      if n.token.kind in ['blank', 'comment']:
        discharge.append(n.token)
        _ = next(p)
        continue
      if current_indent is None:
        if n.token.indent != 0:
          raise FractalTextParseError("Unexpected indentation", n.line_no)
      else:
        if n.token.indent <= current_indent:
          return ItemList([])
      mode = 'list' if n.token.kind == 'value' else 'dict'
      if current_indent is None:
        next_indent = 0
      else:
        next_indent = n.token.indent
      break
    results = []
    while (n := next(p, None)) is not None:
      if n.token.kind in ['blank', 'comment']:
        discharge.append(n.token)
        continue
      if n.token.indent > next_indent:
        raise FractalTextParseError("Unexpected indentation", n.line_no)
      elif n.token.indent < next_indent:
        p.prepend(n)
        break
      if mode == 'list':
        if n.token.kind != 'value':
          raise FractalTextParseError("Mixing of value and key lines is not allowed", n.line_no)
        results.append(ElemAList(discharge, n.token.quoted, n.token.content))
        discharge = []
      elif mode == 'dict':
        if n.token.kind != 'key':
          raise FractalTextParseError("Mixing of value and key lines is not allowed", n.line_no)
        prev_discharge = discharge
        discharge = []
        v = parse_item(next_indent)
        results.append(ElemADict(prev_discharge, n.token.content, v))
    if mode == 'list':
      return ItemAList(next_indent, results)
    elif mode == 'dict':
      return ItemADict(next_indent, results)
  # Ensure that no unexpected tokens remain after parsing the document.
  item = parse_item(None)
  while (n := next(tokens, None)) is not None:
    if n.token.kind in ['blank', 'comment']:
      discharge.append(n.token)
    else:
      raise FractalTextParseError("Unexpected token after parsing complete document", n.line_no)
  if len(discharge) > 0 and discharge[-1].kind == 'blank':
    sts = discharge[:-1]
  else:
    sts = discharge
  return DocumentA(item, sts)


def parse(text: str) -> DocumentA:
  """
  Main entry point for parsing a FractalText document.
  The entire input must correspond to a single Item.
  """
  lines = re.split('\n|\r\n?', text)
  tokens = tokenize(lines)
  return parse_document(tokens)

def load(f: TextIO) -> ItemA:
  return parse(f.read())

def parse_naked(text: str) -> Item:
  return peel(parse(text))

def load_naked(f: TextIO) -> Item:
  return parse_naked(f.read())
