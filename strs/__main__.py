from .commands import *
from .plugins import *
from .core import NAME


del analyze, default, more, validate, string, transform


def _main():
  from fire import Fire as _Fire

  len = length

  if __name__ == '__main__':
    _Fire(name=NAME)

  else:
    _Fire()


if __name__ == "__main__":
  _main()
