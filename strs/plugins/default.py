from __future__ import annotations

from typing import Iterable

from emoji import emojize, demojize, emoji_count
from nth_py.nth import exclude_lines as _exclude_lines, gen_lines as _gen_lines
from unidecode import unidecode

from strs.core import Args, Items, StrSep, SAME_LINE, EMPTY_STR, ErrResult, Peekable, NoResult
from strs.core.base import _gen_sbob_chars

from strs.core.decorators import _wrap_parse_print, _wrap_check_exit
from strs.core.process import _output_items
from strs.core.input import _get_strings_sep, _get_stdin


to_ascii = _wrap_parse_print(unidecode)
to_emoji = _wrap_parse_print(emojize)
from_emoji = _wrap_parse_print(demojize)
has_emoji = _wrap_check_exit(emoji_count)


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


@_output_items
def nth(*line_nums: list[int], exclude: bool = False) -> Items[StrSep]:
  """
  Print lines on `line_nums` from standard input. Setting the `exclude` flag
  will instead print all lines from standard input and lines `line_nums`
  will be excluded.
  """
  stdin = _get_stdin()

  if not (stdin and line_nums):
    yield ErrResult
    return

  lines: Iterable[str] | Peekable[str]

  if exclude:
    lines = _exclude_lines(line_nums, stdin)

  else:
    lines = _gen_lines(line_nums, stdin)

  lines = Peekable[str](lines)

  if lines.is_empty:
    yield NoResult

  yield from map(StrSep, lines)