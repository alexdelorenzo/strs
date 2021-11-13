#!/usr/bin/env bash
from typing import List, Iterable, \
  NamedTuple, Callable
from functools import wraps
# from itertools import chain
# import logging
import sys
import os

import fire


NEW_LINE: str = '\n'
SAME_LINE = EMPTY_STR = ''
SPACE: str = '\t'
SH_SEP: str | None = os.environ.get('IFS')

NO_RESULT: int = -1


Strings = Iterable[str]
Args = List[str]
Input = Strings | Args
ParseStrFunc = Callable[[str, ...], str]


class StringsSep(NamedTuple):
  strings: Strings
  sep: str


def _is_pipeline() -> bool:
  return not sys.stdin.isatty()


def _get_sep() -> str:
  if SH_SEP is not None:
    return SH_SEP

  return NEW_LINE if _is_pipeline() else SPACE


def _decode_strip(line: bytes) -> str:
  string = line.decode()
  return string.strip()


def _get_strings() -> Strings | None:
  if _is_pipeline():
    return map(_decode_strip, sys.stdin.buffer)

  return None


def _get_input(strings: Args) -> Input:
  if stdin := _get_strings():
    strings = stdin

  return strings


def _get_strings_sep(strings: Args) -> StringsSep:
  strings = _get_input(strings)
  sep = _get_sep()

  return StringsSep(strings, sep)


def _wrap_str_parser(func: ParseStrFunc) -> Callable:
  def new_func(*args: Args):
    strings, sep = _get_strings_sep(args)
    _apply(func, strings, sep)

  return new_func


def _apply(
  func: ParseStrFunc,
  strings: Strings,
  sep: str,
  *args,
  **kwargs
):
  for string in strings:
    parsed = func(string, *args, **kwargs)
    print(parsed, end=sep)


def length(*args: Args) -> int:
  strings, sep = _get_strings_sep(args)
  sep_size = len(sep)

  total = sum(
    len(string) + sep_size
    for string in strings
  )

  return total - sep_size


def count(sub: str | None = None, *args: Args) -> int:
  if sub is None or sub == EMPTY_STR:
    return NO_RESULT

  strings, _ = _get_strings_sep(args)

  return sum(
    string.count(sub)
    for string in strings
  )


def index(
  sub: str | None = None,
  *args: Args,
  start: int | None = None,
  end: int | None = None,
) -> int:
  if sub is None or sub == EMPTY_STR:
    return NO_RESULT

  strings, sep = _get_strings_sep(args)
  match_index: int | None
  index: int = 0

  for string in strings:
    line = f'{string}{sep}'

    try:
      match_index = line.index(sub)

    except ValueError:
      match_index = None

    if match_index is not None:
      return index + match_index

    index += len(line)


def split(on: str | None = None, *args: Args):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    split_strs = string.split(sep=on)

    for split_str in split_strs:
      if not split_str:
        continue

      print(f'"{split_str}"', end=sep)


def join(on: str | None = None, *args: Args):
  strings, _ = _get_strings_sep(args)
  sep = on or EMPTY_STR
  first: bool = True

  for string in strings:
    if first:
      print(string, end=SAME_LINE)
      first = False
      continue

    print(f'{sep}{string}', end=SAME_LINE)


upper = _wrap_str_parser(str.upper)
lower = _wrap_str_parser(str.lower)
capitalize = _wrap_str_parser(str.capitalize)
casefold = _wrap_str_parser(str.casefold)


if __name__ == "__main__":
  fire.Fire()
