from __future__ import annotations
from typing import Iterable, NamedTuple, Callable, Any, \
  TypeVar, Generic, Final, NoReturn, ParamSpec, Type, \
  Literal
import logging
import sys

from .types import Args, ErrCode, Result, Items, StrSep, \
  ErrResult, IntError, NoResult, Error, Ok, InputStrsSep, \
  NotFound, Peekable, RepeatTimes, P, T


_process_item: QuitFunc[Item[T]]

def _process_item(item: Item[T]):
  match item:
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


def _get_name(func: Callable) -> str:
  return func.__name__

