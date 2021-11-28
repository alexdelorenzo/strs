from __future__ import annotations
from functools import partial
from itertools import cycle

from emoji import emoji_count, demojize, emojize
from nth_py.nth import gen_lines, exclude_lines
from unidecode import unidecode

from .base import Args, Chars, _get_strings_sep, _wrap_check_exit, \
  _wrap_parse_print, _use_docstring, _cycle_times, _check_exit, \
  SAME_LINE, SPACE, NEW_LINE, EMPTY_STR, FOREVER, ALL, NO_RESULT, \
  ErrCode, _get_stdin, Result, _handle_result


ErrNoResult = Result[int](NO_RESULT, ErrCode.err)
ErrResult = Result(code=ErrCode.err)


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


def length(*args: Args) -> int:
  """ Return the length of the string. """
  strings, sep = _get_strings_sep(args)
  sep_size = len(sep)

  total = sum(
    len(string) + sep_size
    for string in strings
  )

  return total - sep_size


_slice = slice


def slice(
  stop: int,
  *args: Args,
  start: int | None = None,
  step: int | None = None,
):
  """Return substrings using given indices."""
  strings, sep = _get_strings_sep(args)
  window = _slice(start, stop, step)

  for string in strings:
    print(string[window], end=sep)


@_handle_result
def repeat(
  times: int = FOREVER,
  *args: Args,
) -> Result:
  """Repeat string. Set `times` to -1 to repeat forever."""
  if not times:
    return ErrResult

  strings, sep = _get_strings_sep(args)

  if times > FOREVER:
    strings = _cycle_times(strings, times)

  elif times == FOREVER:
    strings = cycle(strings)

  else:
    return ErrResult

  for string in strings:
    print(string, end=sep)


@_check_exit
def contains(
  find: str,
  *args: Args,
) -> bool:
  """Confirm whether the input contains a given string."""
  strings, sep = _get_strings_sep(args)

  for string in strings:
    line = f'{string}{sep}'

    if find in line:
      return True

  return False


@_handle_result
@_use_docstring(str.count)
def count(sub: str, *args: Args) -> Result[int]:
  if sub is None or sub == EMPTY_STR:
    return ErrResult

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
    return ErrResult

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
    return ErrResult

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


@_use_docstring(str.split)
def split(on: str = NEW_LINE, *args: Args):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    split_strs = string.split(sep=on)

    for split_str in split_strs:
      if not split_str:
        continue

      print(split_str, end=sep)


@_use_docstring(str.rsplit)
def rsplit(on: str = NEW_LINE, *args: Args):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    split_strs = string.rsplit(sep=on)

    for split_str in split_strs:
      if not split_str:
        continue

      print(split_str, end=sep)


@_use_docstring(str.join)
def join(on: str = EMPTY_STR, *args: Args):
  strings, _ = _get_strings_sep(args)

  first = next(strings)
  print(first, end=SAME_LINE)

  for string in strings:
    print(f'{on}{string}', end=SAME_LINE)


@_use_docstring(str.strip)
def strip(chars: str | None = None, *args: Args):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.strip(chars)
    print(string, end=sep)


@_use_docstring(str.lstrip)
def lstrip(chars: str | None = None, *args: Args):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.lstrip(chars)
    print(string, end=sep)


@_use_docstring(str.rstrip)
def rstrip(chars: str | None = None, *args: Args):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.rstrip(chars)
    print(string, end=sep)


@_use_docstring(str.expandtabs)
def expandtabs(*args: Args, tabsize: int = 8):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.expandtabs(tabsize)
    print(string, end=sep)


@_use_docstring(str.ljust)
def ljust(width: int, *args: Args, fillchar: str = SPACE):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.ljust(width, fillchar)
    print(string, end=sep)


@_use_docstring(str.rjust)
def rjust(width: int, *args: Args, fillchar: str = SPACE):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.rjust(width, fillchar)
    print(string, end=sep)


@_use_docstring(str.zfill)
def zfill(width: int, *args: Args):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.zfill(width)
    print(string, end=sep)


@_use_docstring(str.partition)
def partition(sep: str, *args: Args):
  strings, _ = _get_strings_sep(args)
  parts: tuple[str, str, str]

  for string in strings:
    parts = string.partition(sep)
    output = NEW_LINE.join(parts)
    print(output)


@_use_docstring(str.rpartition)
def rpartition(sep: str, *args: Args):
  strings, _ = _get_strings_sep(args)
  parts: tuple[str, str, str]

  for string in strings:
    parts = string.rpartition(sep)
    output = NEW_LINE.join(parts)
    print(output)


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
  first = next(iter(strings))

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
    return ErrResult

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
    return ErrResult

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


@_use_docstring(str.center)
def center(
  width: int,
  *args: Args,
  fillchar: str = SPACE,
):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.center(width, fillchar)
    print(string, end=sep)


@_use_docstring(str.replace)
def replace(
  old: str,
  new: str,
  *args: Args,
  count: int = ALL
):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.replace(old, new, count)
    print(string, end=sep)


replace_first = _use_docstring(replace)(
  partial(replace, count=1)
)


def _gen_chars(chars: Chars, reverse: bool) -> Chars:
  caps: bool = reverse

  for char in chars:
    if not char.isalpha():
      yield char
      continue

    char: str = char.upper() if caps else char.lower()
    yield char

    caps = not caps


def sbob(
  *args: Args,
  reverse: bool = False,
):
  """tYpE lIkE tHiS"""
  strings, sep = _get_strings_sep(args)

  for string in strings:
    for char in _gen_chars(string, reverse):
      print(char, end=SAME_LINE)

    print(EMPTY_STR, end=sep)


def nth(*line_nums: list[int], exclude: bool = False):
  """
  Print line numbers `line_nums` from standard input. Setting the `exclude` flag
  will instead print all lines from standard input and lines `line_nums`
  will be excluded.
  """
  stdin = _get_stdin()

  if not (stdin and line_nums):
    raise SystemExit(ErrCode.err)

  if exclude:
    lines = exclude_lines(line_nums, stdin)

  else:
    lines = gen_lines(line_nums, stdin)

  for line in lines:
    print(line)


@_use_docstring(str.format)
def format(*args: Args, **kwargs):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    result = string.format(**kwargs)
    print(result, end=sep)

  raise NotImplementedError()


@_use_docstring(str.format_map)
def format_map(**kwargs):
  print(kwargs)
  raise NotImplementedError()
