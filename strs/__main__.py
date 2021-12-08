from .commands import *
from .plugins import *
from .core import NAME


del analyze, default, more, validate, string, transform


class T:
  def print(self):
    print('test')


def _main():
  from fire import Fire as _Fire
  ___doc___ = 'test'
  len = length

  if __name__ == '__main__':
    _Fire(name=NAME)

  else:
    _Fire()


if __name__ == "__main__":
  _main()
