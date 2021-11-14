from typing import List, Iterable, \
  NamedTuple, Callable
from functools import wraps
# import enum
# import logging
import sys
import os


NEW_LINE: str = '\n'
SAME_LINE = EMPTY_STR = ''
SPACE: str = ' '
SH_SEP: str | None = os.environ.get('IFS')

NO_RESULT: int = -1


Strings = Iterable[str]
Args = List[str]
Input = Strings | Args
ParseStrFunc = Callable[[str, ...], str]
StrCheckFunc = Callable[[str], bool]


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


def _wrap_str_check(func: StrCheckFunc) -> Callable:
  @wraps(func)
  def new_func(*args: Args) -> bool:
    strings, _ = _get_strings_sep(args)

    return all(map(func, strings))

  return new_func


def _wrap_str_parser(func: ParseStrFunc) -> Callable:
  @wraps(func)
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

