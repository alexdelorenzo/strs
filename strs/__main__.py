from .commands import *
from .plugins import *


del analyze, default, more, validate, string, transform


def _main():
  from fire import Fire as _Fire

  len = length

  _Fire()


if __name__ == "__main__":
  _main()
