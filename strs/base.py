from __future__ import annotations
from typing import Iterable, NamedTuple, Callable, Any, \
  TypeVar, Generic
from dataclasses import dataclass
from functools import partial, wraps
from enum import IntEnum, auto
import sys
import os

from strenum import StrEnum
from unpackable import Unpackable


NEW_LINE: str = '\n'
EMPTY_STR: str = ''
SAME_LINE: str = EMPTY_STR
SPACE: str = ' '
DOCTEST: str = '>>>'
SH_SEP: str | None = os.environ.get('IFS')
SLICE_SEP: str = ':'

NO_RESULT: int = -1
MIN_TIMES: int = 1
FIRST: int = 1
INCREMENT: int = 1
FOREVER: int = -1
ALL: int = -1


Decorator = Callable[Callable, Callable]
StrParseFunc = Callable[[str, ...], str]
StrCheckFunc = Callable[str, bool]
CheckFunc = Callable[..., bool]
QuitFunc = Callable[..., None]
Chars = Iterable[str]
Strings = Iterable[str]
Args = list[str]
Input = Strings | Args
T = TypeVar('T')


class StrSep(NamedTuple):
  string: str | None = None
  sep: str = NEW_LINE


class StringsSep(NamedTuple):
  strings: Strings | None
  sep: str


class ErrCode(IntEnum):
  """Shell return codes"""
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


class CmdState(StrEnum):
  ok: str = auto()
  err: str = auto()
  quit: str = auto()


@dataclass
class Result(Generic[T], Unpackable):
  result: T | None = None
  code: ErrCode = ErrCode.ok
  state: CmdState = CmdState.ok


StreamResult = Result | StrSep | ErrCode | None
StreamingResults = Iterable[StreamResult]
GenFunc = Callable[..., StreamingResults]
ResultFunc = Callable[..., Result[Any]]


ErrResult = Result(code=ErrCode.err)
ErrIntResult = Result[int](NO_RESULT, ErrCode.err)


def _is_pipeline() -> bool:
  return not sys.stdin.isatty()


def _get_sep() -> str:
  if SH_SEP is not None:
    return SH_SEP

  return EMPTY_STR if _is_pipeline() else NEW_LINE
  # return NEW_LINE


def _parse_line(line: bytes, strip: bool = False) -> str:
  string = line.decode()
  # string = string.rstrip(NEW_LINE)

  if strip:
    return string.strip()

  return string


def _get_stdin(strip: bool = False) -> Strings | None:
  if not _is_pipeline():
    return None

  parse = partial(_parse_line, strip=strip)
  return map(parse, sys.stdin.buffer)


def _get_input(args: Args, strip: bool = False) -> Input:
  if stdin := _get_stdin(strip):
    return stdin

  strings = map(str, args)
  return strings


def _get_strings_sep(args: Args, strip: bool = False) -> StringsSep:
  strings = _get_input(args, strip)
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


def _wrap_str_check(func: StrCheckFunc) -> CheckFunc:
  @_use_docstring(func)
  def new_func(*args: Args, **kwargs) -> bool:
    strings, _ = _get_strings_sep(args)

    func_kwargs = partial(func, **kwargs)
    checks = map(func_kwargs, strings)

    return all(checks)

  return new_func


def _check_exit(func: CheckFunc) -> QuitFunc:
  @_use_docstring(func)
  def new_func(*args, **kwargs):
    result: bool = func(*args, **kwargs)
    code = ErrCode.from_bool(result)
    sys.exit(code)

  return new_func


def _wrap_check_exit(func: StrCheckFunc) -> CheckFunc:
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


def _handle_result(func: ResultFunc) -> QuitFunc:
  @wraps(func)
  def new_func(*args, **kwargs):
    result = func(*args, **kwargs)

    if not result:
      sys.exit(ErrCode.ok)

    result, code, *_ = result

    if result:
      print(result)

    sys.exit(code)

  return new_func


def _handle_stream(func: GenFunc) -> QuitFunc:
  @wraps(func)
  def new_func(*args, **kwargs):
    gen: StreamingResults = func(*args, **kwargs)

    for result in gen:
      match result:
        case StrSep(string, sep):
          print(string, end=sep)

        case Result(result, code) if code.is_err:
          if result:
            print(result)

          sys.exit(code)

        case ErrCode() as code:
          sys.exit(code)

        case None:
          sys.exit(ErrCode.err)

    sys.exit(ErrCode.ok)

  return new_func


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


# see https://stackoverflow.com/a/54421070
def _slice_from_str(string: str) -> slice:
  if not string:
    return slice()

  indices: list[str | None] = string.split(SLICE_SEP)

  match indices:
    case [one]:
      indices = [None, one]

  nums = (
    int(index) if index else None
    for index in indices
  )

  return slice(*nums)
