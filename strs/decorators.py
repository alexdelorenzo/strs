from __future__ import annotations
from collections.abc import Iterable as Iter
from functools import partial, wraps
from typing import Iterable, Callable
import logging
import sys

from .constants import NEW_LINE, DOCTEST
from .process import _process_item
from .types import Args, ErrCode, Result, Items, Item, \
  Peekable, P, T


def _to_peekable(
  func: Callable[P, Iterable[T]]
) -> Callable[P, Peekable[T]]:
  @wraps(func)
  def new_func(*args: P.args, **kwargs: P.kwargs) -> Peekable[T]:
    gen = func(*args, **kwargs)
    return Peekable[T](gen)

  return new_func

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


def _wrap_str_check(func: StrCheckFunc) -> CheckFunc[P]:
  @_use_metadata(func)
  def new_func(*args: Args, **kwargs: P.kwargs) -> bool:
    func_kwargs: CheckFunc[P.args] = partial(func, **kwargs)
    strings, _ = _get_strings_sep(args)
    checks = map(func_kwargs, strings)

    return all(checks)

  return new_func


def _wrap_check_exit(func: StrCheckFunc) -> QuitFunc[str]:
  wrapped = _wrap_str_check(func)
  return _handle_item(wrapped)


def _wrap_parse_print(func: StrParseFunc[P]) -> QuitFunc[P]:
  @_use_metadata(func)
  def new_func(*args: Args):
    strings, sep = _get_strings_sep(args)
    _apply(func, strings, sep)

    sys.exit(ErrCode.ok)

  return new_func


def _handle_item(func: ItemFunc[P, T]) -> QuitFunc[P]:
  @wraps(func)
  def new_func(*args: P.args, **kwargs: P.kwargs):
    result = func(*args, **kwargs)
    _process_item(result)

    sys.exit(ErrCode.ok)

  return new_func


def _output_items(func: ItemsFunc[P, T] | ItemFunc[P, T]) -> QuitFunc[P]:
  @wraps(func)
  def new_func(*args: P.args, **kwargs: P.kwargs):
    results: Items[T] | Item[T] = \
      func(*args, **kwargs)

    match results:
      case Iter():
        results = Peekable[Item[T]](results)

      case Result() | _ as item:
        _process_item(item)
        return

    if results.is_empty:
      logging.debug(f'No results found for {_get_name(func)}.')
      sys.exit(ErrCode.no_result)

    for result in results:
      _process_item(result)

    sys.exit(ErrCode.ok)

  return new_func


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


def _apply(
  func: StrParseFunc[P],
  strings: Strings,
  sep: str,
  *args: P.args,
  **kwargs: P.kwargs,
):
  for string in strings:
    parsed = func(string, *args, **kwargs)
    print(parsed, end=sep)

