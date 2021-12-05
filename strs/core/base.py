from __future__ import annotations
from typing import Iterable, NamedTuple, Callable, Any, \
  TypeVar, Generic, Final, NoReturn, ParamSpec, Type, \
  Literal
from collections.abc import Iterable as Iter
from dataclasses import dataclass
from functools import partial, wraps
from enum import IntEnum, auto
import logging
import sys
import os

from unpackable import Unpackable
from more_itertools import peekable

from .constants import SAME_LINE, SPACE, NEW_LINE, EMPTY_STR, \
  FOREVER, ALL, FIRST, NO_CMD_ERR, START_INDEX, NO_ITEMS, \
  NOT_FOUND, MIN_TIMES, SH_SEP

from .types import Chars, T, RepeatTimes, _to_peekable

FOREVER_OPTS: Final[set[str]] = set(RepeatTimes.__args__)


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


# see https://docs.python.org/3/library/itertools.html#itertools.cycle
def _cycle_times(
  iterable: Iterable[T],
  times: int = MIN_TIMES,
) -> Iterable[T]:
  """Cycle through iterable `times` times."""
  if times < MIN_TIMES:
    return

  saved: list[T] = []

  for element in iterable:
    yield element
    saved.append(element)

  cycles: int = FIRST

  while saved and cycles < times:
    for element in saved:
      yield element

    cycles += INCREMENT


# see https://stackoverflow.com/a/54421070
def _slice_from_str(string: str) -> slice:
  if not string:
    return slice(SKIP)

  indices: list[str | SKIP] = string.split(SLICE_SEP)

  match indices:
    case [end]:
      indices = [SKIP, end]

  nums = (
    int(index) if index else SKIP
    for index in indices
  )

  return slice(*nums)
