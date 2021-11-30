import types

# from .commands import capitalize, casefold, length, count, \
#  index, join, split, upper, lower, strip, title, swapcase, \
#  lstrip, rstrip, find, isascii
from .commands import *


def leave_only_cmd_funcs():
  for name, val in globals().copy().items():
    match val:
      case types.FunctionType() | types.MethodType():
        pass

      case mod if mod is types:
        pass

      case _ if not name.startswith('__'):
        del globals()[name]


def _main():
  leave_only_cmd_funcs()

  from fire import Fire as _Fire

  len = length

  _Fire()


if __name__ == "__main__":
  _main()
