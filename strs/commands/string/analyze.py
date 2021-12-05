from __future__ import annotations
import logging

from ...core.constants import EMPTY_STR, START_INDEX, NOT_FOUND
from ...core.decorators import _use_metadata
from ...core.input import _get_strings_sep
from ...core.process import _output_items
from ...core.types import Args, Result, Ok, IntError, NotFound


@_output_items
def length(*args: Args) -> Result[int]:
  """ Return the length of the string."""
  strings, sep = _get_strings_sep(args)
  sep_size = len(sep)

  total = sum(
    len(string) + sep_size
    for string in strings
  )

  total -= sep_size
  return Ok(total)


@_output_items
@_use_metadata(str.count)
def count(sub: str, *args: Args) -> Result[int]:
  if sub is None or sub == EMPTY_STR:
    return IntError

  strings, _ = _get_strings_sep(args)

  total = sum(
    string.count(sub)
    for string in strings
  )

  if not total:
    return NotFound(total)

  return Ok(total)


@_output_items
@_use_metadata(str.index)
def index(
  sub: str,
  *args: Args,
  start: int | None = None,
  end: int | None = None,
) -> Result[int]:
  if sub is None or sub == EMPTY_STR:
    return IntError

  strings, sep = _get_strings_sep(args)
  match_index: int | None
  index: int = START_INDEX

  for string in strings:
    line = f'{string}{sep}'

    try:
      match_index = line.index(sub, start, end)

    except ValueError as e:
      logging.debug(f"Caught ValueError({e})")
      match_index = None

    if match_index is not None:
      index += match_index
      return Ok(index)

    index += len(line)

  return NotFound()


@_output_items
@_use_metadata(str.rindex)
def rindex(
  sub: str,
  *args: Args,
  start: int | None = None,
  end: int | None = None,
) -> Result[int]:
  if sub is None or sub == EMPTY_STR:
    return IntError

  strings, sep = _get_strings_sep(args)
  match_index: int | None
  index: int = START_INDEX

  for string in strings:
    line = f'{string}{sep}'

    try:
      match_index = line.rindex(sub)

    except ValueError:
      match_index = None

    if match_index is not None:
      index += match_index
      return Ok(index)

    index += len(line)

  return NotFound()


@_output_items
@_use_metadata(str.find)
def find(
  sub: str | None = None,
  *args: Args,
  start: int | None = None,
  end: int | None = None,
) -> Result[int]:
  if sub is None or sub == EMPTY_STR:
    return IntError

  strings, sep = _get_strings_sep(args)
  match_index: int | None
  index: int = START_INDEX

  for string in strings:
    line = f'{string}{sep}'
    match_index = line.find(sub, start, end)

    if match_index is not NOT_FOUND:
      index += match_index
      return Ok(index)

    index += len(line)

  return NotFound(NOT_FOUND)


@_output_items
@_use_metadata(str.rfind)
def rfind(
  sub: str | None = None,
  *args: Args,
  start: int | None = None,
  end: int | None = None,
) -> Result[int]:
  if sub is None or sub == EMPTY_STR:
    return IntError

  strings, sep = _get_strings_sep(args)
  match_index: int | None
  index: int = START_INDEX

  for string in strings:
    line = f'{string}{sep}'
    match_index = line.rfind(sub, start, end)

    if match_index is not NOT_FOUND:
      index += match_index
      return Ok(index)

    index += len(line)

  return NotFound(NOT_FOUND)


__all__ = [
  'count',
  'find',
  'index',
  'length',
  'rfind',
  'rindex',
]
