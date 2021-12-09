from __future__ import annotations
from functools import partial

from ...core.constants import SPACE, ALL, FIRST, NEW_LINE, EMPTY_STR, \
  SAME_LINE, NO_CMD_ERR
from ...core.decorators import _wrap_parse_print, _use_metadata
from ...core.process import _output_items
from ...core.input import _get_strings_sep
from ...core.types import Args, Items, StrSep, Result, Ok


upper = _wrap_parse_print(str.upper)
lower = _wrap_parse_print(str.lower)
capitalize = _wrap_parse_print(str.capitalize)
casefold = _wrap_parse_print(str.casefold)
swapcase = _wrap_parse_print(str.swapcase)
title = _wrap_parse_print(str.title)


@_output_items
@_use_metadata(str.center)
def center(
  width: int,
  *args: Args,
  fillchar: str = SPACE,
) -> Items[StrSep]:
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.center(width, fillchar)
    yield StrSep(string, sep)


@_output_items
@_use_metadata(str.replace)
def replace(
  old: str,
  new: str,
  *args: Args,
  count: int = ALL
) -> Items[StrSep]:
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.replace(old, new, count)
    yield StrSep(string, sep)


replace_first = _use_metadata(replace)(
  partial(replace, count=FIRST)
)


@_output_items
@_use_metadata(str.split)
def split(on: str = NEW_LINE, *args: Args) -> Items[StrSep]:
  strings, sep = _get_strings_sep(args)

  if not sep:
    sep = NEW_LINE

  for string in strings:
    string = string.rstrip(NEW_LINE)
    split_strs = string.split(sep=on)

    for split_str in split_strs:
      if not split_str:
        continue

      yield StrSep(split_str, sep)


@_output_items
@_use_metadata(str.rsplit)
def rsplit(on: str = NEW_LINE, *args: Args) -> Items[StrSep]:
  strings, sep = _get_strings_sep(args)

  for string in strings:
    split_strs = string.rsplit(sep=on)

    for split_str in split_strs:
      if not split_str:
        continue

      yield StrSep(split_str, sep)


@_output_items
@_use_metadata(str.join)
def join(
  on: str = EMPTY_STR,
  *args: Args
) -> Items[StrSep | Result[str]]:
  strings, _ = _get_strings_sep(args)
  sep = SAME_LINE

  if first := next(strings, None):
    first = first.rstrip(NEW_LINE)

  elif first is None:
    return

  yield StrSep(first, sep)

  for string in strings:
    string = string.rstrip(NEW_LINE)
    yield StrSep(f'{on}{string}', sep)

  yield Ok(EMPTY_STR)


@_output_items
@_use_metadata(str.strip)
def strip(chars: str | None = None, *args: Args) -> Items[StrSep]:
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.strip(chars)
    yield StrSep(string, sep)


@_output_items
@_use_metadata(str.lstrip)
def lstrip(chars: str | None = None, *args: Args) -> Items[StrSep]:
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.lstrip(chars)
    yield StrSep(string, sep)


@_output_items
@_use_metadata(str.rstrip)
def rstrip(chars: str | None = None, *args: Args) -> Items[StrSep]:
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.rstrip(chars)
    yield StrSep(string, sep)


@_output_items
@_use_metadata(str.expandtabs)
def expandtabs(*args: Args, tabsize: int = 8) -> Items[StrSep]:
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.expandtabs(tabsize)
    yield StrSep(string, sep)


@_output_items
@_use_metadata(str.ljust)
def ljust(width: int, *args: Args, fillchar: str = SPACE) -> Items[StrSep]:
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.ljust(width, fillchar)
    yield StrSep(string, sep)


@_output_items
@_use_metadata(str.rjust)
def rjust(width: int, *args: Args, fillchar: str = SPACE) -> Items[StrSep]:
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.rjust(width, fillchar)
    yield StrSep(string, sep)


@_output_items
@_use_metadata(str.zfill)
def zfill(width: int, *args: Args) -> Items[StrSep]:
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.zfill(width)
    yield StrSep(string, sep)


@_output_items
@_use_metadata(str.partition)
def partition(sep: str, *args: Args) -> Items[StrSep]:
  strings, _ = _get_strings_sep(args)
  parts: tuple[str, str, str]

  for string in strings:
    parts = string.partition(sep)
    output = NEW_LINE.join(parts)
    yield StrSep(output)


@_output_items
@_use_metadata(str.rpartition)
def rpartition(sep: str, *args: Args) -> Items[StrSep]:
  strings, _ = _get_strings_sep(args)
  parts: tuple[str, str, str]

  for string in strings:
    parts = string.rpartition(sep)
    output = NEW_LINE.join(parts)
    yield StrSep(output)


@_use_metadata(str.format)
def format(fmt: str, *args: Args, **kwargs):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    result = string.format(fmt, **kwargs)
    print(result, sep)

  raise NotImplementedError(NO_CMD_ERR)


@_use_metadata(str.format_map)
def format_map(**kwargs):
  raise NotImplementedError(NO_CMD_ERR)


__all__ = [
  'capitalize',
  'casefold',
  'center',
  'expandtabs',
  'format',
  'format_map',
  'join',
  'ljust',
  'lower',
  'lstrip',
  'partition',
  'replace',
  'replace_first',
  'rjust',
  'rpartition',
  'rsplit',
  'rstrip',
  'split',
  'strip',
  'swapcase',
  'title',
  'upper',
  'zfill',
]
