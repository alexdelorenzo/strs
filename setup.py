from setuptools import setup
from pathlib import Path


requirements = \
  Path('requirements.txt') \
    .read_text() \
    .splitlines()


setup(
  name="strs",
  version="0.0.1",
  description="String manipulation methods for the shell",
  url="https://github.com/alexdelorenzo/strs",
  author="Alex DeLorenzo",
  license="AGPL 3.0",
  packages=['strs'],
  zip_safe=True,
  install_requires=requirements,
  entry_points={
    "console_scripts": [
      "strs = strs.__main__:main",
      "str = strs.__main__:main"
      ]
    }
)
