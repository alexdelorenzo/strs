from .cmd import *
from .commands.string import *
from .plugins import *


def _main():
  from fire import Fire as _Fire

  len = length

  _Fire()


if __name__ == "__main__":
  _main()
