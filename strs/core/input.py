from __future__ import annotations
from functools import partial
import sys

from .constants import NEW_LINE, EMPTY_STR, SH_SEP
from .types import Args, InputStrsSep, Input, Strings, \
  Arg, _to_peekable


def _is_pipeline() -> bool:
  return not sys.stdin.isatty()


def _get_sep() -> str:
  if SH_SEP is not None:
    return SH_SEP

  return EMPTY_STR if _is_pipeline() else NEW_LINE


def _get_stdin(strip: bool = False) -> Strings | None:
  if not _is_pipeline():
    return None

  parse = partial(_parse_line, strip=strip)
  return map(parse, sys.stdin.buffer)


@_to_peekable
def _get_input(args: Args, strip: bool = False) -> Input:
  if stdin := _get_stdin(strip):
    return stdin

  strings = map(str, args)
  return strings


def _get_strings_sep(args: Args, strip: bool = False) -> InputStrsSep:
  strings = _get_input(args, strip)
  sep = _get_sep()

  return InputStrsSep(strings, sep)


def _parse_line(line: Arg, strip: bool = False) -> str:
  match line:
    case bytes():
      string = line.decode()

    case int() | float():
      string = str(line)

    case str():
      string = line

    case _:
      raise ValueError(f"Not supported: {line}")

  if strip:
    return string.strip()

  return string
