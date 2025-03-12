from io import StringIO

from hypothesis import example, given
from hypothesis import strategies as st

from fractaltext.annotate import from_dict_naked, to_dict_naked
from fractaltext.item import (
  DocumentA,
  ElemDict,
  ElemList,
  Item,
  ItemDict,
  ItemList,
  should_quote,
)
from fractaltext.parse import parse, parse_naked
from fractaltext.serialize import dump, dump_naked


def serialize_all(doc: DocumentA) -> str:
  with StringIO() as f:
    dump(doc, f)
    return f.getvalue()


def serialize_naked_all(it: Item, isucc: int = 2) -> str:
  with StringIO() as f:
    dump_naked(it, f, isucc)
    return f.getvalue()


@st.composite
def item(draw):
  chars = st.characters(exclude_characters=["\n", "\r"])

  @st.composite
  def elem_list(draw):
    x = draw(st.text(alphabet=chars))
    return ElemList(should_quote(x), x)

  k = draw(st.sampled_from(["list", "dict"]))
  if k == "list":
    els = draw(st.lists(elem_list()))
    return ItemList(els)
  elif k == "dict":
    deds = draw(st.dictionaries(st.text(alphabet=chars), item(), min_size=1))
    res = []
    for key, value in deds.items():
      res.append(ElemDict(key, value))
    return ItemDict(res)


class TestProp:
  @given(item())
  @example(ItemList([]))
  @example(ItemDict([ElemDict("", ItemList([]))]))
  def test_id(self, it: Item):
    assert parse_naked(serialize_naked_all(it)) == it

  @given(item())
  @example(ItemList([]))
  @example(ItemDict([ElemDict("", ItemList([]))]))
  def test_id2(self, it: Item):
    assert serialize_naked_all(
      parse_naked(serialize_naked_all(it))
    ) == serialize_naked_all(it)

  @given(item())
  @example(ItemList([]))
  @example(ItemDict([ElemDict("", ItemList([]))]))
  def test_id3(self, it: Item):
    assert serialize_all(parse(serialize_naked_all(it))) == serialize_naked_all(it)

  @given(item())
  @example(ItemList([]))
  @example(ItemDict([ElemDict("", ItemList([]))]))
  def test_id4(self, it: Item):
    assert from_dict_naked(to_dict_naked(it)) == it

  @given(item())
  @example(ItemList([]))
  @example(ItemDict([ElemDict("", ItemList([]))]))
  def test_id5(self, it: Item):
    assert to_dict_naked(from_dict_naked(to_dict_naked(it))) == to_dict_naked(it)

  def test_id6(self):
    ss = [
      """\
# comment 1
:key
  # comment 2
  value
  # comment 3
""",
      """\
:key1
  value1
  value2
:key2
  # comment1
  # comment2
""",
    ]
    for s in ss:
      assert serialize_all(parse(s)) == s
