from __future__ import annotations
from functools import partial
from itertools import cycle

from emoji import emoji_count, demojize, emojize
from nth_py.nth import gen_lines as _gen_lines, \
  exclude_lines as _exclude_lines
from unidecode import unidecode

from .base import Args, _get_strings_sep, _wrap_check_exit, \
  _wrap_parse_print, _use_docstring, _cycle_times, _check_exit, \
  SAME_LINE, SPACE, NEW_LINE, EMPTY_STR, FOREVER, ALL, ErrCode, \
  _get_stdin, Result, _handle_result, FIRST, StreamResults, \
  _handle_stream, StrSep, ErrResult, ErrIntResult, _is_pipeline, \
  _slice_from_str, _gen_sbob_chars, _get_name, NO_CMD_ERR


upper = _wrap_parse_print(str.upper)
lower = _wrap_parse_print(str.lower)
capitalize = _wrap_parse_print(str.capitalize)
casefold = _wrap_parse_print(str.casefold)
swapcase = _wrap_parse_print(str.swapcase)
title = _wrap_parse_print(str.title)


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


to_ascii = _wrap_parse_print(unidecode)
to_emoji = _wrap_parse_print(emojize)
from_emoji = _wrap_parse_print(demojize)
has_emoji = _wrap_check_exit(emoji_count)

del unidecode, emojize, demojize, emoji_count


@_handle_result
def length(*args: Args) -> Result[int]:
  """ Return the length of the string."""
  strings, sep = _get_strings_sep(args)
  sep_size = len(sep)

  total = sum(
    len(string) + sep_size
    for string in strings
  )

  total -= sep_size
  return Result(total)


_slice = slice


@_handle_stream
def substring(
  stop: int,
  *args: Args,
  start: int | None = None,
  step: int | None = None,
) -> StreamResults:
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


@_handle_stream
def slice(
  indices: str,
  *args: Args,
) -> StreamResults:
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


@_handle_stream
def repeat(
  times: int = FOREVER,
  *args: Args,
) -> StreamResults:
  """Repeat string. Set `times` to -1 to repeat forever."""
  if not times:
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


@_check_exit
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


@_handle_result
@_use_docstring(str.count)
def count(sub: str, *args: Args) -> Result[int]:
  if sub is None or sub == EMPTY_STR:
    return ErrIntResult

  strings, _ = _get_strings_sep(args)

  total = sum(
    string.count(sub)
    for string in strings
  )

  return Result(total)


@_handle_result
@_use_docstring(str.index)
def index(
  sub: str,
  *args: Args,
  start: int | None = None,
  end: int | None = None,
) -> Result[int]:
  if sub is None or sub == EMPTY_STR:
    return ErrIntResult

  strings, sep = _get_strings_sep(args)
  match_index: int | None
  index: int = 0

  for string in strings:
    line = f'{string}{sep}'

    try:
      match_index = line.index(sub, start, end)

    except ValueError:
      match_index = None

    if match_index is not None:
      index += match_index
      return Result(index)

    index += len(line)


@_handle_result
@_use_docstring(str.rindex)
def rindex(
  sub: str,
  *args: Args,
  start: int | None = None,
  end: int | None = None,
) -> Result[int]:
  if sub is None or sub == EMPTY_STR:
    return ErrIntResult

  strings, sep = _get_strings_sep(args)
  match_index: int | None
  index: int = 0

  for string in strings:
    line = f'{string}{sep}'

    try:
      match_index = line.rindex(sub)

    except ValueError:
      match_index = None

    if match_index is not None:
      index += match_index
      return Result(index)

    index += len(line)


@_handle_stream
@_use_docstring(str.split)
def split(on: str = NEW_LINE, *args: Args) -> StreamResults:
  strings, sep = _get_strings_sep(args)

  for string in strings:
    split_strs = string.split(sep=on)

    for split_str in split_strs:
      if not split_str:
        continue

      yield StrSep(split_str, sep)


@_handle_stream
@_use_docstring(str.rsplit)
def rsplit(on: str = NEW_LINE, *args: Args) -> StreamResults:
  strings, sep = _get_strings_sep(args)

  for string in strings:
    split_strs = string.rsplit(sep=on)

    for split_str in split_strs:
      if not split_str:
        continue

      yield StrSep(split_str, sep)


@_handle_stream
@_use_docstring(str.join)
def join(on: str = EMPTY_STR, *args: Args) -> StreamResults:
  strings, _ = _get_strings_sep(args)

  first = next(strings).rstrip(NEW_LINE)
  yield StrSep(first, SAME_LINE)

  for string in strings:
    string = string.rstrip(NEW_LINE)
    yield StrSep(f'{on}{string}', SAME_LINE)


@_handle_stream
@_use_docstring(str.strip)
def strip(chars: str | None = None, *args: Args) -> StreamResults:
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.strip(chars)
    yield StrSep(string, sep)


@_handle_stream
@_use_docstring(str.lstrip)
def lstrip(chars: str | None = None, *args: Args) -> StreamResults:
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.lstrip(chars)
    yield StrSep(string, sep)


@_handle_stream
@_use_docstring(str.rstrip)
def rstrip(chars: str | None = None, *args: Args) -> StreamResults:
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.rstrip(chars)
    yield StrSep(string, sep)


@_handle_stream
@_use_docstring(str.expandtabs)
def expandtabs(*args: Args, tabsize: int = 8) -> StreamResults:
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.expandtabs(tabsize)
    yield StrSep(string, sep)


@_handle_stream
@_use_docstring(str.ljust)
def ljust(width: int, *args: Args, fillchar: str = SPACE) -> StreamResults:
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.ljust(width, fillchar)
    yield StrSep(string, sep)


@_handle_stream
@_use_docstring(str.rjust)
def rjust(width: int, *args: Args, fillchar: str = SPACE) -> StreamResults:
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.rjust(width, fillchar)
    yield StrSep(string, sep)


@_handle_stream
@_use_docstring(str.zfill)
def zfill(width: int, *args: Args) -> StreamResults:
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.zfill(width)
    yield StrSep(string, sep)


@_handle_stream
@_use_docstring(str.partition)
def partition(sep: str, *args: Args) -> StreamResults:
  strings, _ = _get_strings_sep(args)
  parts: tuple[str, str, str]

  for string in strings:
    parts = string.partition(sep)
    output = NEW_LINE.join(parts)
    yield StrSep(output)


@_handle_stream
@_use_docstring(str.rpartition)
def rpartition(sep: str, *args: Args) -> StreamResults:
  strings, _ = _get_strings_sep(args)
  parts: tuple[str, str, str]

  for string in strings:
    parts = string.rpartition(sep)
    output = NEW_LINE.join(parts)
    yield StrSep(output)


@_check_exit
@_use_docstring(str.endswith)
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


@_check_exit
@_use_docstring(str.startswith)
def startswith(
  prefix: str | tuple[str, ...],
  *args: Args,
  start: int | None = None,
  end: int | None = None,
) -> bool:
  strings, _ = _get_strings_sep(args)
  strings = iter(strings)
  first = next(strings, None)

  if first is None:
    return False

  return first.startswith(prefix, start, end)


@_handle_result
@_use_docstring(str.find)
def find(
  sub: str | None = None,
  *args: Args,
  start: int | None = None,
  end: int | None = None,
) -> Result[int]:
  if sub is None or sub == EMPTY_STR:
    return ErrIntResult

  strings, sep = _get_strings_sep(args)
  match_index: int | None
  index: int = 0

  for string in strings:
    line = f'{string}{sep}'
    match_index = line.find(sub, start, end)

    if match_index is not None:
      index += match_index
      return Result(index)

    index += len(line)


@_handle_result
@_use_docstring(str.rfind)
def rfind(
  sub: str | None = None,
  *args: Args,
  start: int | None = None,
  end: int | None = None,
) -> Result[int]:
  if sub is None or sub == EMPTY_STR:
    return ErrIntResult

  strings, sep = _get_strings_sep(args)
  match_index: int | None
  index: int = 0

  for string in strings:
    line = f'{string}{sep}'
    match_index = line.rfind(sub, start, end)

    if match_index is not None:
      index += match_index
      return Result(index)

    index += len(line)


@_handle_stream
@_use_docstring(str.center)
def center(
  width: int,
  *args: Args,
  fillchar: str = SPACE,
) -> StreamResults:
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.center(width, fillchar)
    yield StrSep(string, sep)


@_handle_stream
@_use_docstring(str.replace)
def replace(
  old: str,
  new: str,
  *args: Args,
  count: int = ALL
) -> StreamResults:
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.replace(old, new, count)
    yield StrSep(string, sep)


replace_first = _use_docstring(replace)(
  partial(replace, count=FIRST)
)


@_handle_stream
def sbob(
  *args: Args,
  reverse: bool = False,
) -> StreamResults:
  """tYpE lIkE tHiS"""
  strings, sep = _get_strings_sep(args)

  for string in strings:
    chars = _gen_sbob_chars(string, reverse)

    for char in chars:
      yield StrSep(char, SAME_LINE)

    yield StrSep(EMPTY_STR, sep)


@_handle_stream
def nth(*line_nums: list[int], exclude: bool = False) -> StreamResults:
  """
  Print lines on `line_nums` from standard input. Setting the `exclude` flag
  will instead print all lines from standard input and lines `line_nums`
  will be excluded.
  """
  stdin = _get_stdin()

  if not (stdin and line_nums):
    yield ErrResult
    return

  if exclude:
    lines = _exclude_lines(line_nums, stdin)

  else:
    lines = _gen_lines(line_nums, stdin)

  yield from map(StrSep, lines)


@_use_docstring(str.format)
def format(fmt: str, *args: Args, **kwargs):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    result = string.format(fmt, **kwargs)
    print(result, sep)

  raise NotImplementedError(NO_CMD_ERR)


@_use_docstring(str.format_map)
def format_map(**kwargs):
  raise NotImplementedError(NO_CMD_ERR)


__all__ = [
  'capitalize',
  'casefold',
  'center',
  'contains',
  'count',
  'endswith',
  'expandtabs',
  'find',
  'format',
  'format_map',
  'from_emoji',
  'has_emoji',
  'index',
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
  'join',
  'length',
  'ljust',
  'lower',
  'lstrip',
  'nth',
  'partition',
  'repeat',
  'replace',
  'rfind',
  'rindex',
  'rjust',
  'rpartition',
  'rsplit',
  'rstrip',
  'sbob',
  'slice',
  'split',
  'startswith',
  'strip',
  'sub',
  'substring',
  'swapcase',
  'title',
  'to_ascii',
  'to_emoji',
  'upper',
  'zfill',
]