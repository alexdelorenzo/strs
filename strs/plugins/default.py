from __future__ import annotations
from typing import Iterable, Pattern, TextIO, Sequence, Final
import re

from emoji import demojize, emoji_count, emojize
from unidecode import unidecode

from ..core.base import first, _get_window
from ..core.constants import EMPTY_STR, NEW_LINE, SAME_LINE, WHITESPACE_RE, \
  SPACE, LOWEST
from ..core.decorators import _wrap_check_exit, _wrap_parse_print
from ..core.input import _get_stdin, _get_strings_sep
from ..core.process import _output_items
from ..core.types import Args, Chars, ErrResult, Items, NoResult, Peekable, \
  StrSep, _to_peekable, StrCheckFunc


LineNums = Sequence[int]


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
    lines = _exclude_lines(line_nums, stdin)

  else:
    lines = _gen_lines(line_nums, stdin)

  lines = Peekable[str](lines)

  if lines.is_empty:
    yield NoResult
    return

  for line in lines:
    yield StrSep(line, SAME_LINE)


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
  match sep:
    case str():
      sep: Pattern[str] = re.compile(sep)

  strings, _ = _get_strings_sep(args, strip=False)

  if not (item := strings.peek(None)):
    return

  match sep.findall(item):
    case [*seps] if any(seps):
      tab = first(seps)

  window = _get_window(num)
  end_col = window

  if isinstance(window, slice):
    end_col: int | None = None if window.stop is None else window.stop - 1

  no_end: bool = end_col is None
  no_result: bool = True

  for string in strings:
    cols: list[str] = [c for c in sep.split(string) if c]
    can_slice: bool = no_end or len(cols) >= abs(end_col)

    if can_slice and (output := cols[window]):
      yield StrSep(output, NEW_LINE)
      no_result = False

  if no_result:
    yield NoResult


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


@_to_peekable
def _gen_lines(
  line_nums: LineNums,
  content: TextIO,
) -> Iterable[str]:
  nums = sorted(line_nums)

  for nth, line in enumerate(content):
    if nth == nums[LOWEST]:
      yield line
      del nums[LOWEST]

      if not nums:
        break


@_to_peekable
def _exclude_lines(
  line_nums: LineNums,
  content: TextIO,
) -> Iterable[str]:
  nums = set(line_nums)

  for nth, line in enumerate(content):
    if nth not in nums:
      yield line

    else:
      nums.remove(nth)


__all__ = [
  'col',
  'from_emoji',
  'has_emoji',
  'nth',
  'sbob',
  'to_ascii',
  'to_emoji',
]
