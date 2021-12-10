from __future__ import annotations
from typing import Iterable, Pattern
import re

from emoji import demojize, emoji_count, emojize
from nth_py.nth import exclude_lines, gen_lines
from unidecode import unidecode
from first import first

from ..core.base import _slice_from_str
from ..core.constants import EMPTY_STR, NEW_LINE, SAME_LINE, WHITESPACE_RE, SPACE
from ..core.decorators import _wrap_check_exit, _wrap_parse_print
from ..core.input import _get_stdin, _get_strings_sep
from ..core.process import _output_items
from ..core.types import Args, Chars, ErrResult, Items, NoResult, Peekable, \
  StrSep, _to_peekable


to_ascii = _wrap_parse_print(unidecode)
to_emoji = _wrap_parse_print(emojize)
from_emoji = _wrap_parse_print(demojize)
has_emoji = _wrap_check_exit(emoji_count)


@_output_items
def nth(*line_nums: int, exclude: bool = False) -> Items[StrSep]:
  """
  Print lines on `line_nums` from standard input.

  Setting the `exclude` flag will instead print all lines from standard input and lines `line_nums`
  will be excluded.
  """
  stdin = _get_stdin()

  if not (stdin and line_nums):
    yield ErrResult
    return

  line_nums: list[int]  # keep mypy quiet
  lines: Iterable[str] | Peekable[str]

  if exclude:
    lines = exclude_lines(line_nums, stdin)

  else:
    lines = gen_lines(line_nums, stdin)

  lines = Peekable[str](lines)

  if lines.is_empty:
    yield NoResult
    return

  yield from map(StrSep, lines)


@_output_items
def col(
  num: int | str,
  *args: Args,
  sep: str | Pattern[str] = WHITESPACE_RE,
) -> Items[StrSep]:
  """
  Return the string in the column specified by `num`.

  Set `sep` to change the column separator from the whitespace regex default.

  Column specified by `num` can be negative and you can use Python's `slice` syntax.
  """
  if isinstance(sep, str):
    sep: Pattern[str] = re.compile(sep)

  strings, _ = _get_strings_sep(args, strip=False)
  tab: str = SPACE

  if not (item := strings.peek()):
    return

  match sep.findall(item):
    case [*seps] if any(seps):
      tab = first(seps)

  window = _get_window(num)
  end_col: int | None = None if window.stop is None else window.stop - 1
  no_end: bool = not end_col
  no_result: bool = True

  for string in strings:
    cols: list[str] = [c for c in sep.split(string) if c]

    if no_end or len(cols) >= abs(end_col):
      cols = cols[window]
      output: str = tab.join(cols)
      yield StrSep(output, NEW_LINE)

      no_result = False

  if no_result:
    yield NoResult


def _get_window(num: str | int) -> slice:
  if isinstance(num, str):
    return _slice_from_str(num)

  elif isinstance(num, int):
    index: int = num if num <= 0 else num - 1
    return slice(index, index + 1)

  raise ValueError


@_output_items
def sbob(
  *args: Args,
  reverse: bool = False,
) -> Items[StrSep]:
  """tYpE lIkE tHiS"""
  strings, sep = _get_strings_sep(args)

  for string in strings:
    chars = _gen_sbob_chars(string, reverse)

    for char in chars:
      yield StrSep(char, SAME_LINE)

    yield StrSep(EMPTY_STR, sep)


@_to_peekable
def _gen_sbob_chars(chars: Chars, reverse: bool = False) -> Chars:
  caps: bool = reverse

  for char in chars:
    if not char.isalpha():
      yield char
      continue

    char = char.upper() if caps else char.lower()
    yield char

    caps = not caps


__all__ = [
  'col',
  'from_emoji',
  'has_emoji',
  'nth',
  'sbob',
  'to_ascii',
  'to_emoji',
]
