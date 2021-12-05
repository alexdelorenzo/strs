from __future__ import annotations

from emoji import emoji_count, demojize, emojize
from unidecode import unidecode

from ...core.constants import NO_CMD_ERR
from ...core.decorators import _use_metadata
from ...core.input import _get_strings_sep
from ...core.types import Args

del unidecode, emojize, demojize, emoji_count

_slice = slice


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
  'format',
  'format_map',
]
