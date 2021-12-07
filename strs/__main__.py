from .commands import *
from .plugins import *


del analyze, default, more, validate, string, transform


class T:
  def print(self):
    print('test')


def _main():
  from fire import Fire as _Fire
  ___doc___ = 'test'
  len = length

  _Fire()
  # _Fire(T)


if __name__ == "__main__":
  _main()
