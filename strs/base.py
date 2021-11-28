from __future__ import annotations
from typing import Iterable, NamedTuple, Callable, Any, \
  TypeVar, Generic
from dataclasses import dataclass
from functools import partial
from enum import IntEnum
import sys
import os

from unpackable import Unpackable


NEW_LINE: str = '\n'
EMPTY_STR: str = ''
SAME_LINE: str = EMPTY_STR
SPACE: str = ' '
DOCTEST: str = '>>>'
SH_SEP: str | None = os.environ.get('IFS')

NO_RESULT: int = -1
MIN_TIMES: int = 1
FIRST: int = 1
INCREMENT: int = 1
FOREVER: int = -1
ALL: int = -1


Decorator = Callable[Callable, Callable]
StrParseFunc = Callable[[str, ...], str]
StrCheckFunc = Callable[str, bool]
QuitFunc = Callable[..., None]
Chars = Iterable[str]
Strings = Iterable[str]
Args = list[str]
Input = Strings | Args
T = TypeVar('T')


class StringsSep(NamedTuple):
  strings: Strings
  sep: str


class ErrCode(IntEnum):
  ok: int = 0
  err: int = 1

  true: int = ok
  false: int = err

  @staticmethod
  def from_bool(other: bool) -> ErrCode:
    return ErrCode.true if other else ErrCode.false

  @property
  def is_err(self) -> bool:
    return self != ErrCode.ok


@dataclass
class Result(Generic[T], Unpackable):
  result: T | None = None
  code: ErrCode = ErrCode.ok


ResultFunc = Callable[..., Result[Any]]


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


def _get_stdin() -> Strings | None:
  if not _is_pipeline():
    return None

  return map(_parse_line, sys.stdin.buffer)


def _get_input(args: Args) -> Input:
  if stdin := _get_stdin():
    return stdin

  strings = map(str, args)
  return strings


def _get_strings_sep(args: Args) -> StringsSep:
  strings = _get_input(args)
  sep = _get_sep()

  return StringsSep(strings, sep)


def _strip_doctests(string: str | None) -> str | None:
  if string is None:
    return

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
  def new_func(*args: Args, **kwargs) -> bool:
    strings, _ = _get_strings_sep(args)

    func_kwargs = partial(func, **kwargs)
    checks = map(func_kwargs, strings)

    return all(checks)

  return new_func


def _check_exit(func: Callable) -> QuitFunc:
  @_use_docstring(func)
  def new_func(*args, **kwargs):
    result: bool = func(*args, **kwargs)
    rc = ErrCode.from_bool(result)
    sys.exit(rc)

  return new_func


def _handle_result(func: ResultFunc) -> QuitFunc:
  @_use_docstring(func)
  def new_func(*args, **kwargs):
    result = func(*args, **kwargs)

    if not result:
      sys.exit(ErrCode.ok)

    result, code = result

    if result:
      print(result)

    sys.exit(code)

  return new_func


def _wrap_check_exit(func: StrCheckFunc) -> Callable[..., bool]:
  wrapped = _wrap_str_check(func)
  return _check_exit(wrapped)


def _wrap_parse_print(func: StrParseFunc) -> Callable[..., None]:
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

  cycles: int = FIRST

  while saved and cycles < times:
    for element in saved:
      yield element

    cycles += INCREMENT
