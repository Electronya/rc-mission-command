import json
from unittest import TestCase
from unittest.mock import Mock, call, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

import app      # noqa: E402


class TestApp(TestCase):
    """
    The app module test cases.
    """
