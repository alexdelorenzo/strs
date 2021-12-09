from .commands import *
from .plugins import *
from .core import NAME


def _main():
  from fire import Fire as _Fire

  len = length  # command alias

  if __name__ == '__main__':
    _Fire(name=NAME)

  else:
    _Fire()


if __name__ == "__main__":
  _main()
