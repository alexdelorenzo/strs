from __future__ import annotations
from typing import Final

import os


NEW_LINE: Final[str] = '\n'
EMPTY_STR: Final[str] = ''
SAME_LINE: Final[str] = EMPTY_STR
SPACE: Final[str] = ' '
DOCTEST: Final[str] = '>>>'
SLICE_SEP: Final[str] = ':'
SH_SEP: Final[str | None] = os.environ.get('IFS')

START_INDEX: Final[int] = 0
MIN_TIMES: Final[int] = 1
FIRST: Final[int] = 1
INCREMENT: Final[int] = 1

NOT_FOUND: int = -1
NO_RESULT: Final[int] = -1
FOREVER: Final[int] = -1
ALL: Final[int] = -1
SKIP: Final[None] = None
NO_ITEMS: Final[Ellipsis] = ...

NO_CMD_ERR: Final[str] = "This command isn't implemented."
WHITESPACE_RE: Final[str] = r'\s'
