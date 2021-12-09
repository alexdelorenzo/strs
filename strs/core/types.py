from __future__ import annotations
from typing import Iterable, NamedTuple, Callable, Any, \
    TypeVar, Generic, NoReturn, ParamSpec, Type, Literal, \
    Sequence, Final
from functools import wraps
from enum import IntEnum, auto
from dataclasses import dataclass

from more_itertools import peekable
from strenum import StrEnum
from unpackable import Unpackable

from .constants import NEW_LINE, NO_RESULT


RepeatTimes = Literal['forever', 'inf', 'infinite', 'loop']
ColumnSeps = Literal['tab', 'newline', 'space']


FOREVER_OPTS: Final[set[str]] = set(RepeatTimes.__args__)
COL_OPTS: Final[dict[str, str]] = {
  'tab': '\t',
  'newline': '\n',
  'space': ' ',
}


T = TypeVar('T')
P = ParamSpec('P')

Decorator = Callable[[Callable[P, T]], Callable[P, T]]
StrParseFunc = Callable[[str, P], str]
StrCheckFunc = Callable[[str], bool | int]
CheckFunc = Callable[P, bool]
QuitFunc = Callable[P, NoReturn]

Chars = Iterable[str]
Arg = str | int | float
Args = Sequence[Arg]


class Peekable(Generic[T], peekable):
  """Generic and typed `peekable` with convenience methods."""
  iterable: Iterable[T]

  @property
  def is_empty(self) -> bool:
    return not self


Strings = Peekable[str] | Iterable[str]
Input = Strings | Args


class InputStrsSep(NamedTuple):
  strings: Strings | None
  sep: str


class StrSep(NamedTuple):
  string: str | None = None
  sep: str = NEW_LINE


class ErrCode(IntEnum):
  """Shell return codes."""
  none: int = -1

  ok: int = 0
  err: int = 1

  no_result: int = 2
  no_handler: int = 3

  found: int = ok
  not_found: int = 4
  bad_input: int = 5

  true: int = ok
  false: int = err

  @classmethod
  def from_bool(cls: Type[ErrCode], other: bool) -> ErrCode:
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
  # state: CmdState = CmdState.ok


@dataclass
class Ok(Result[T]):
  code: ErrCode = ErrCode.ok


@dataclass
class Error(Result[T]):
  code: ErrCode = ErrCode.err


@dataclass
class NotFound(Error[T]):
  code: ErrCode = ErrCode.not_found


@dataclass
class BadInput(Error[T]):
  code: ErrCode = ErrCode.bad_input


Item = T | Result[T] | StrSep | ErrCode | int | bool | None
Items = Iterable[Item[T]] | Peekable[Item[T]]

ItemsFunc = Callable[P, Items[T] | Item[T]]
ItemFunc = Callable[P, Result[Item[T] | T | Any]]


NoResult = Result[None](code=ErrCode.no_result)
NoneFound = NotFound[None]()

ErrResult = Error[None]()
IntError = BadInput[int](NO_RESULT)


def _to_peekable(
  func: Callable[P, Iterable[T]]
) -> Callable[P, Peekable[T]]:
  @wraps(func)
  def new_func(*args: P.args, **kwargs: P.kwargs) -> Peekable[T]:
    gen: Iterable[T] = func(*args, **kwargs)
    return Peekable[T](gen)

  return new_func
