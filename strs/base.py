from typing import Iterable, NamedTuple, Callable
import sys
import os


NEW_LINE: str = '\n'
EMPTY_STR: str = ''
SAME_LINE: str = EMPTY_STR
SPACE: str = ' '
DOCTEST: str = '>>>'
SH_SEP: str | None = os.environ.get('IFS')

NO_RESULT: int = -1
MIN_TIMES: int = 1
FOREVER: int = -1


Decorator = Callable[Callable, Callable]
StrParseFunc = Callable[[str, ...], str]
StrCheckFunc = Callable[str, bool]
Chars = Iterable[str]
Strings = Iterable[str]
Args = list[str]
Input = Strings | Args


class StringsSep(NamedTuple):
  strings: Strings
  sep: str


def _is_pipeline() -> bool:
  return not sys.stdin.isatty()


def _get_sep() -> str:
  if SH_SEP is not None:
    return SH_SEP

  # return NEW_LINE if _is_pipeline() else SPACE
  return NEW_LINE


def _parse_line(line: bytes, strip: bool = False) -> str:
  string = line.decode()
  string = string.rstrip(NEW_LINE)

  if strip:
    return string.strip()

  return string


def _get_strings() -> Strings | None:
  if _is_pipeline():
    return map(_parse_line, sys.stdin.buffer)

  return None


def _get_input(strings: Args) -> Input:
  if stdin := _get_strings():
    return stdin

  strings = map(str, strings)
  return strings


def _get_strings_sep(strings: Args) -> StringsSep:
  strings = _get_input(strings)
  sep = _get_sep()

  return StringsSep(strings, sep)


def _strip_doctests(string: str) -> str:
  if DOCTEST not in string:
    return string

  docs: list[str] = []
  lines = string.split(NEW_LINE)

  for line in lines:
    if DOCTEST in line:
      break

    docs.append(line)

  return NEW_LINE.join(docs)


def _use_docstring(source: Callable | str) -> Decorator:
  if isinstance(source, Callable):
    source: str = _strip_doctests(source.__doc__)

  def decorator(to_func: Callable) -> Callable:
    to_func.__doc__ = source
    return to_func

  return decorator


def _wrap_str_check(func: StrCheckFunc) -> Callable[..., bool]:
  @_use_docstring(func)
  def new_func(*args: Args) -> bool:
    strings, _ = _get_strings_sep(args)
    checks = map(func, strings)
    return all(checks)

  return new_func


def _wrap_str_parser(func: StrParseFunc) -> Callable[..., None]:
  @_use_docstring(func)
  def new_func(*args: Args):
    strings, sep = _get_strings_sep(args)
    _apply(func, strings, sep)

  return new_func


def _apply(
  func: StrParseFunc,
  strings: Strings,
  sep: str,
  *args,
  **kwargs
):
  for string in strings:
    parsed = func(string, *args, **kwargs)
    print(parsed, end=sep)


# see: https://docs.python.org/3/library/itertools.html#itertools.cycle
def _cycle_times(
  iterable: Iterable,
  times: int = MIN_TIMES,
) -> Iterable:
  """Cycle through iterable `times` times."""
  if times < MIN_TIMES:
    return

  saved = []

  for element in iterable:
    yield element
    saved.append(element)

  cycles: int = 1

  while saved and cycles < times:
    for element in saved:
      yield element

    cycles += 1
