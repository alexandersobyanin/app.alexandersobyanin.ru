#!python3

import os
import sys

if sys.version_info[0] < 3:
    raise Exception("Python3 required! Current: {0}".format(sys.version_info))

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lsd import app as application
