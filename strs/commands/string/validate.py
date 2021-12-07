from __future__ import annotations

from ...core.decorators import _wrap_check_exit, _use_metadata
from ...core.input import _get_strings_sep
from ...core.process import _output_items
from ...core.types import Args


isalnum = _wrap_check_exit(str.isalnum)
isalpha = _wrap_check_exit(str.isalpha)
isascii = _wrap_check_exit(str.isascii)
isdecimal = _wrap_check_exit(str.isdecimal)
isdigit = _wrap_check_exit(str.isdigit)
isidentifier = _wrap_check_exit(str.isidentifier)
islower = _wrap_check_exit(str.islower)
isnumeric = _wrap_check_exit(str.isnumeric)
isprintable = _wrap_check_exit(str.isprintable)
isspace = _wrap_check_exit(str.isspace)
istitle = _wrap_check_exit(str.istitle)
isupper = _wrap_check_exit(str.isupper)


@_output_items
@_use_metadata(str.endswith)
def endswith(
  suffix: str | tuple[str, ...],
  *args: Args,
  start: int | None = None,
  end: int | None = None,
) -> bool:
  strings, _ = _get_strings_sep(args)
  string: str | None = None

  for string in strings:
    pass

  if string is not None:
    return string.endswith(suffix, start, end)

  return False


@_output_items
@_use_metadata(str.startswith)
def startswith(
  prefix: str | tuple[str, ...],
  *args: Args,
  start: int | None = None,
  end: int | None = None,
) -> bool:
  strings, _ = _get_strings_sep(args)

  if strings.is_empty:
    return False

  first = next(strings)

  return first.startswith(prefix, start, end)


__all__ = [
  'endswith',
  'isalnum',
  'isalpha',
  'isascii',
  'isdecimal',
  'isdigit',
  'isidentifier',
  'islower',
  'isnumeric',
  'isprintable',
  'isspace',
  'istitle',
  'isupper',
  'startswith',
]
