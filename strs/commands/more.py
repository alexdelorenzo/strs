from __future__ import annotations
from itertools import cycle

from ..core.base import _slice_from_str, _cycle_times
from ..core.constants import NEW_LINE, SAME_LINE, FOREVER
from ..core.input import _get_strings_sep
from ..core.process import _output_items
from ..core.types import Args, Items, StrSep, RepeatTimes, ErrResult, \
  FOREVER_OPTS


_slice = slice


@_output_items
def substring(
  stop: int,
  *args: Args,
  start: int | None = None,
  step: int | None = None,
) -> Items[StrSep]:
  """Return substrings using given indices."""
  strings, _ = _get_strings_sep(args)
  window = _slice(start, stop, step)

  for string in strings:
    sub = string[window]

    if sub.endswith(NEW_LINE):
      sep = SAME_LINE

    else:
      sep = NEW_LINE

    yield StrSep(sub, sep)


sub = substring


@_output_items
def slice(
  indices: str,
  *args: Args,
) -> Items[StrSep]:
  """Return substrings using given indices."""
  strings, _ = _get_strings_sep(args)
  window = _slice_from_str(indices)

  for string in strings:
    sub = string[window]

    if sub.endswith(NEW_LINE):
      sep = SAME_LINE

    else:
      sep = NEW_LINE

    yield StrSep(sub, sep)


@_output_items
def repeat(
  times: int | RepeatTimes = FOREVER,
  *args: Args,
) -> Items[StrSep]:
  """Repeat string. Set `times` to -1 to repeat forever."""
  match times:
    case str() as s if s.casefold() in FOREVER_OPTS:
      times: int = FOREVER

    case None | 0:
      yield ErrResult
      return

  strings, sep = _get_strings_sep(args)

  if times > FOREVER:
    strings = _cycle_times(strings, times)

  elif times == FOREVER:
    strings = cycle(strings)

  else:
    yield ErrResult
    return

  for string in strings:
    yield StrSep(string, sep)


@_output_items
def contains(
  find: str,
  *args: Args,
  case_sensitive: bool = True
) -> bool:
  """Confirm whether the input contains a given string."""
  find = str(find)

  if not case_sensitive:
    find = find.casefold()

  strings, sep = _get_strings_sep(args)

  for string in strings:
    line = f'{string}{sep}'

    if not case_sensitive:
      line = line.casefold()

    if find in line:
      return True

  return False


__all__ = [
  'contains',
  'slice',
  'substring',
  'repeat',
]
