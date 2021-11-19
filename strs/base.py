from typing import List, Iterable, \
  NamedTuple, Callable
import sys
import os


SH_SEP: str | None = os.environ.get('IFS')

NEW_LINE: str = '\n'
EMPTY_STR: str = ''
SAME_LINE: str = EMPTY_STR
SPACE: str = ' '

NO_RESULT: int = -1


ParseStrFunc = Callable[[str, ...], str]
StrCheckFunc = Callable[str, bool]
Strings = Iterable[str]
Args = List[str]
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


def _decode_strip(line: bytes) -> str:
  string = line.decode()
  return string.strip()


def _get_strings() -> Strings | None:
  if _is_pipeline():
    return map(_decode_strip, sys.stdin.buffer)

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


def _use_docstring(from_func: Callable) -> Callable[Callable, Callable]:
  def decorator(to_func: Callable) -> Callable:
    to_func.__doc__ = from_func.__doc__

    return to_func

  return decorator


def _wrap_str_check(func: StrCheckFunc) -> Callable[..., bool]:
  @_use_docstring(func)
  def new_func(*args: Args) -> bool:
    strings, _ = _get_strings_sep(args)
    checks = map(func, strings)

    return all(checks)

  return new_func


def _wrap_str_parser(func: ParseStrFunc) -> Callable[..., None]:
  @_use_docstring(func)
  def new_func(*args: Args):
    strings, sep = _get_strings_sep(args)
    _apply(func, strings, sep)

  return new_func


def _apply(
  func: ParseStrFunc,
  strings: Strings,
  sep: str,
  *args,
  **kwargs
):
  for string in strings:
    parsed = func(string, *args, **kwargs)
    print(parsed, end=sep)
