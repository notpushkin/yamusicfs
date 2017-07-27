import sys
import logging

from . import fs

logging.basicConfig(level=logging.DEBUG)
fs.run(sys.argv[1], foreground=True)
