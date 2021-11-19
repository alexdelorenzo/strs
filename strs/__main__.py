from .commands import capitalize, casefold, length, count, \
  index, join, split, upper, lower, strip, title, swapcase, \
  lstrip, rstrip, find, isascii

from .commands import *
del Args


def main():
  from fire import Fire

  len = length

  Fire()


if __name__ == "__main__":
  main()
