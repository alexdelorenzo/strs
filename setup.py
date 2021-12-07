from setuptools import setup, find_packages
from pathlib import Path


requirements: list[str] = \
  Path('requirements.txt') \
    .read_text() \
    .splitlines()

pkgs: list[str] = find_packages(
  include=[
    'strs',
    'strs.*',
  ]
)


setup(
  name="strs",
  version="0.1.0",
  description="🧵 String manipulation tools for the shell",
  url="https://github.com/alexdelorenzo/strs",
  author="Alex DeLorenzo",
  license="AGPL 3.0",
  packages=pkgs,
  zip_safe=True,
  install_requires=requirements,
  entry_points={
    "console_scripts": [
      "strs = strs.__main__:_main",
      "str = strs.__main__:_main",
    ]
  }
)
