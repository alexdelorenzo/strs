#!/usr/bin/env python
# from itertools import chain
# import logging

from base import Args, _get_strings_sep, _wrap_str_check, \
  _wrap_str_parser, EMPTY_STR, NO_RESULT, SAME_LINE, SPACE, \
  NEW_LINE

import fire


def length(*args: Args) -> int:
  strings, sep = _get_strings_sep(args)
  sep_size = len(sep)

  total = sum(
    len(string) + sep_size
    for string in strings
  )

  return total - sep_size


def count(sub: str | None = None, *args: Args) -> int:
  if sub is None or sub == EMPTY_STR:
    return NO_RESULT

  strings, _ = _get_strings_sep(args)

  return sum(
    string.count(sub)
    for string in strings
  )


def index(
  sub: str | None = None,
  *args: Args,
  start: int | None = None,
  end: int | None = None,
) -> int:
  if sub is None or sub == EMPTY_STR:
    return NO_RESULT

  strings, sep = _get_strings_sep(args)
  match_index: int | None
  index: int = 0

  for string in strings:
    line = f'{string}{sep}'

    try:
      match_index = line.index(sub)

    except ValueError:
      match_index = None

    if match_index is not None:
      return index + match_index

    index += len(line)


def rindex(
  sub: str | None = None,
  *args: Args,
  start: int | None = None,
  end: int | None = None,
) -> int:
  if sub is None or sub == EMPTY_STR:
    return NO_RESULT

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
      return index + match_index

    index += len(line)


def split(on: str | None = None, *args: Args):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    split_strs = string.split(sep=on)

    for split_str in split_strs:
      if not split_str:
        continue

      print(split_str, end=sep)


def rplit(on: str | None = None, *args: Args):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    split_strs = string.rsplit(sep=on)

    for split_str in split_strs:
      if not split_str:
        continue

      print({split_str}, end=sep)


def join(on: str | None = None, *args: Args):
  strings, _ = _get_strings_sep(args)
  sep = on or EMPTY_STR
  first: bool = True

  for string in strings:
    if first:
      print(string, end=SAME_LINE)
      first = False
      continue

    print(f'{sep}{string}', end=SAME_LINE)


def strip(chars: str | None = None, *args: Args):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.strip(chars)
    print(string, end=sep)


def lstrip(chars: str | None = None, *args: Args):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.lstrip(chars)
    print(string, end=sep)


def rstrip(chars: str | None = None, *args: Args):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.rstrip(chars)
    print(string, end=sep)


def expandtabs(*args: Args, tabsize: int = 8):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.expandtabs(tabsize)
    print(string, end=sep)


def ljust(width: int, *args: Args, fillchar: str = SPACE):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.ljust(width, fillchar)
    print(string, end=sep)


def rjust(width: int, *args: Args, fillchar: str = SPACE):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.rjust(width, fillchar)
    print(string, end=sep)


def zfill(width: int, *args: Args):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.zfill(width)
    print(string, end=sep)


def partition(sep: str, *args: Args):
  strings, _ = _get_strings_sep(args)
  parts: tuple[str, str, str]

  for string in strings:
    parts = string.partition(sep)
    output = NEW_LINE.join(parts)
    print(output)


def rpartition(sep: str, *args: Args):
  strings, _ = _get_strings_sep(args)
  parts: tuple[str, str, str]

  for string in strings:
    parts = string.rpartition(sep)
    output = NEW_LINE.join(parts)
    print(output)


def endswith(
  suffix: str | tuple[str, ...],
  *args: Args,
  start: int | None = None,
  end: int | None = None,
):
  strings, _ = _get_strings_sep(args)

  for string in strings:
    pass

  return string.endswith(suffix, start, end)


def startswith(
  prefix: str | tuple[str, ...],
  *args: Args,
  start: int | None = None,
  end: int | None = None,
):
  strings, _ = _get_strings_sep(args)
  first = next(iter(strings))

  return first.startswith(prefix, start, end)


def find(
  sub: str | None = None,
  *args: Args,
  start: int | None = None,
  end: int | None = None,
) -> int:
  if sub is None or sub == EMPTY_STR:
    return NO_RESULT

  strings, sep = _get_strings_sep(args)
  match_index: int | None
  index: int = 0

  for string in strings:
    line = f'{string}{sep}'

    match_index = line.find(sub, start, end)

    if match_index is not None:
      return index + match_index

    index += len(line)


def rfind(
  sub: str | None = None,
  *args: Args,
  start: int | None = None,
  end: int | None = None,
) -> int:
  if sub is None or sub == EMPTY_STR:
    return NO_RESULT

  strings, sep = _get_strings_sep(args)
  match_index: int | None
  index: int = 0

  for string in strings:
    line = f'{string}{sep}'

    match_index = line.rfind(sub, start, end)

    if match_index is not None:
      return index + match_index

    index += len(line)


def center(
  width: int,
  fillchar: str = SPACE,
  *args: Args
):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.center(width, fillchar)
    print(string, end=sep)


def replace(new: str, *args: Args, count: int = -1):
  strings, sep = _get_strings_sep(args)

  for string in strings:
    string = string.replace(new, count)
    print(string, end=sep)


upper = _wrap_str_parser(str.upper)
lower = _wrap_str_parser(str.lower)
capitalize = _wrap_str_parser(str.capitalize)
casefold = _wrap_str_parser(str.casefold)
title = _wrap_str_parser(str.title)
swapcase = _wrap_str_parser(str.swapcase)


isalnum = _wrap_str_check(str.isalnum)
isalpha = _wrap_str_check(str.isalpha)
isascii = _wrap_str_check(str.isascii)
isdecimal = _wrap_str_check(str.isdecimal)
isdigit = _wrap_str_check(str.isdigit)
isidentifier = _wrap_str_check(str.isidentifier)
islower = _wrap_str_check(str.islower)
isnumeric = _wrap_str_check(str.isnumeric)
isprintable = _wrap_str_check(str.isprintable)
isspace = _wrap_str_check(str.isspace)
istitle = _wrap_str_check(str.istitle)
isupper = _wrap_str_check(str.isupper)


if __name__ == "__main__":
  fire.Fire()
