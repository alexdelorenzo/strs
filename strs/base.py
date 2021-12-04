from __future__ import annotations
from typing import Iterable, NamedTuple, Callable, Any, \
  TypeVar, Generic, Final
from dataclasses import dataclass
from functools import partial, wraps
from enum import IntEnum, auto
import sys
import os

from strenum import StrEnum
from unpackable import Unpackable
from more_itertools import peekable


NEW_LINE: Final[str] = '\n'
EMPTY_STR: Final[str] = ''
SAME_LINE: Final[str] = EMPTY_STR
SPACE: Final[str] = ' '
DOCTEST: Final[str] = '>>>'
SH_SEP: Final[str | None] = os.environ.get('IFS')
SLICE_SEP: Final[str] = ':'

START_INDEX: Final[int] = 0
MIN_TIMES: Final[int] = 1
FIRST: Final[int] = 1
INCREMENT: Final[int] = 1

NO_RESULT: Final[int] = -1
FOREVER: Final[int] = -1
ALL: Final[int] = -1
SKIP: Final[None] = None
NO_ITEMS: Final[None] = None

NO_CMD_ERR: Final[str] = "This command doesn't exist yet."


T = TypeVar('T')
Decorator = Callable[Callable[..., T], Callable[..., T]]
StrParseFunc = Callable[[str, ...], str]
StrCheckFunc = Callable[str, bool]
CheckFunc = Callable[..., bool]
QuitFunc = Callable[..., None]
Chars = Iterable[str]
Strings = Iterable[str]
Args = list[str | int]
Input = Strings | Args


class InputStrsSep(NamedTuple):
  strings: Strings | None
  sep: str


class StrSep(NamedTuple):
  string: str | None = None
  sep: str = NEW_LINE


class ErrCode(IntEnum):
  """Shell return codes"""
  none: int = -1

  ok: int = 0
  err: int = 1

  no_result: int = 2
  no_handler: int = 3

  not_found: int = 4
  found: int = ok

  true: int = ok
  false: int = err

  @classmethod
  def from_bool(cls: type, other: bool) -> ErrCode:
    return cls.true if other else cls.false

  @property
  def is_err(self) -> bool:
    if self == ErrCode.none:
      return False

    return self != ErrCode.ok

  @property
  def should_quit(self) -> bool:
    return self != ErrCode.none


class CmdState(StrEnum):
  ok: str = auto()
  err: str = auto()
  quit: str = auto()


@dataclass
class Result(Generic[T], Unpackable):
  result: T | None = None
  code: ErrCode = ErrCode.none
  state: CmdState = CmdState.ok


@dataclass
class Error(Result[T]):
  code: ErrCode = ErrCode.err


@dataclass
class Ok(Result[T]):
  code: ErrCode = ErrCode.ok


@dataclass
class NotFound(Error[T]):
  code: ErrCode = ErrCode.not_found


StreamResult = T | Result[T] | StrSep | ErrCode | None
ResultStream = Iterable[StreamResult[T]]
ResultsFunc = Callable[..., ResultStream[T] | StreamResult[T]]
ResultFunc = Callable[..., Result[T | Any]]


NoResult = Result[None](code=ErrCode.no_result)
NotFoundResult = NotFound()

ErrResult = Error()
IntError = Error[int](NO_RESULT)


def _is_pipeline() -> bool:
  return not sys.stdin.isatty()


def _get_sep() -> str:
  if SH_SEP is not None:
    return SH_SEP

  return EMPTY_STR if _is_pipeline() else NEW_LINE


def _parse_line(line: bytes, strip: bool = False) -> str:
  string = line.decode()

  if strip:
    return string.strip()

  return string


def _get_stdin(strip: bool = False) -> Strings | None:
  if not _is_pipeline():
    return None

  parse = partial(_parse_line, strip=strip)
  return map(parse, sys.stdin.buffer)


def _to_peekable(
  func: Callable[..., Iterable[T]]
) -> Callable[..., Iterable[T]]:
  @wraps(func)
  def new_func(*args, **kwargs) -> Iterable:
    gen = func(*args, **kwargs)
    return peekable(gen)

  return new_func


@_to_peekable
def _get_input(args: Args, strip: bool = False) -> Input:
  if stdin := _get_stdin(strip):
    return stdin

  strings = map(str, args)
  return strings


def _get_strings_sep(args: Args, strip: bool = False) -> InputStrsSep:
  strings = _get_input(args, strip)
  sep = _get_sep()

  return InputStrsSep(strings, sep)


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


def _use_metadata(source: Callable | str, name: str = True) -> Decorator:
  is_callable: bool = isinstance(source, Callable)

  if is_callable:
    docs: str = _strip_doctests(source.__doc__)

  else:
    docs = source

  func_name: str | None = None

  if name and is_callable:
    func_name = source.__name__

  def decorator(to_func: Callable) -> Callable:
    to_func.__doc__ = docs

    if name and func_name:
      to_func.__name__ = func_name

    return to_func

  return decorator


def _wrap_str_check(func: StrCheckFunc) -> CheckFunc:
  @_use_metadata(func)
  def new_func(*args: Args, **kwargs) -> bool:
    strings, _ = _get_strings_sep(args)
    func_kwargs = partial(func, **kwargs)

    checks = map(func_kwargs, strings)
    return all(checks)

  return new_func


def _wrap_check_exit(func: StrCheckFunc) -> QuitFunc:
  wrapped = _wrap_str_check(func)
  return _handle_result(wrapped)


def _wrap_parse_print(func: StrParseFunc) -> QuitFunc:
  @_use_metadata(func)
  def new_func(*args: Args):
    strings, sep = _get_strings_sep(args)
    _apply(func, strings, sep)

    sys.exit(ErrCode.ok)

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
    _process_result(result)

    sys.exit(ErrCode.ok)

  return new_func


_process_result: QuitFunc
def _process_result(result: StreamResult):
  match result:
    case Result((string, sep), code):
      if string is not None:
        print(string, end=sep)

      if code.should_quit:
        sys.exit(code)

    case Result(result=bool()) | bool() as result:
      code = ErrCode.from_bool(result)
      sys.exit(code)

    case Result(result, code):
      if result is not None:
        print(result)

      if code.should_quit:
        sys.exit(code)

    case StrSep(string, sep):
      print(string, end=sep)

    case ErrCode() as code if code.should_quit:
      sys.exit(code)

    case None:
      logging.debug(f'No result from handler.')
      sys.exit(ErrCode.no_result)

    case _rest:
      logging.error(f'No handler for {_get_name(type(_rest))}.')
      sys.exit(ErrCode.no_handler)


def _handle_results(func: ResultsFunc[T] | ResultFunc[T]) -> QuitFunc:
  @wraps(func)
  def new_func(*args, **kwargs):
    results: ResultStream[T] | StreamResult[T] = \
      func(*args, **kwargs)

    if not isinstance(results, Iterable):
      _process_result(results)
      return

    results: ResultStream[T] = peekable(results)

    if results.peek(NO_ITEMS) is NO_ITEMS:
      logging.debug(f'No results found with {_get_name(func)}.')
      sys.exit(ErrCode.no_result)

    for result in results:
      _process_result(result)

    sys.exit(ErrCode.ok)

  return new_func


def _gen_sbob_chars(chars: Chars, reverse: bool = False) -> Chars:
  caps: bool = reverse

  for char in chars:
    if not char.isalpha():
      yield char
      continue

    char = char.upper() if caps else char.lower()
    yield char

    caps = not caps


def _get_name(func: Callable) -> str:
  return func.__name__


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
