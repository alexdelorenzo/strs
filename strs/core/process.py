from __future__ import annotations
from functools import wraps
from typing import Callable
from collections.abc import Iterable
import logging
import sys

from .types import ErrCode, Result, StrSep, QuitFunc, Item, T, \
  ItemsFunc, P, ItemFunc, Items, Peekable


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


def _output_items(func: ItemsFunc[P, T] | ItemFunc[P, T]) -> QuitFunc[P]:
  @wraps(func)
  def new_func(*args: P.args, **kwargs: P.kwargs):
    items: Items[T] | Item[T] = \
      func(*args, **kwargs)

    match items:
      case Result() as item:
        _process_item(item)
        return

      case Iterable():
        items = Peekable[Item[T]](items)

      case _ as item:
        _process_item(item)
        return

    if items.is_empty:
      logging.debug(f'No results found for {_get_name(func)}.')
      sys.exit(ErrCode.no_result)

    for item in items:
      _process_item(item)

    sys.exit(ErrCode.ok)

  return new_func
