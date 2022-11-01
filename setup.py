from setuptools import setup, find_packages
from pathlib import Path


requirements: list[str] = (
  Path('requirements.txt')
  .read_text()
  .splitlines()
)

pkgs: list[str] = find_packages(
  # include=[
  #  'strs',
  #  'strs.*',
  # ]
)


setup(
  name="strs",
  version="0.3.0",
  description="🧵 Easy string tools for the shell",
  url="https://github.com/alexdelorenzo/strs",
  author="Alex DeLorenzo (alexdelorenzo.dev)",
  license="AGPL 3.0",
  packages=pkgs,
  install_requires=requirements,
  python_requires='>=3.11',
  entry_points={
    "console_scripts": [
      "strs = strs.__main__:_main",
      "str = strs.__main__:_main",
    ]
  }
)
