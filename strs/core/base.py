from __future__ import annotations
from typing import Iterable

from .constants import FIRST, MIN_TIMES, INCREMENT, SKIP, SLICE_SEP
from .types import T


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
