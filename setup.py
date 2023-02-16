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

main: str = 'strs.__main__:_main'

setup(
  name="strs",
  version="0.4.0",
  description="Easy string tools for the shell",
  url="https://github.com/alexdelorenzo/strs",
  author="Alex DeLorenzo (alexdelorenzo.dev)",
  license="AGPL 3.0",
  packages=pkgs,
  install_requires=requirements,
  python_requires='>=3.10',
  entry_points={
    "console_scripts": [
      f"strs = {main}",
      f"str = {main}",
    ]
  }
)
