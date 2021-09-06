import json
from unittest import TestCase
from unittest.mock import Mock, call, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))
mockedPygame = Mock()
sys.modules['pygame'] = mockedPygame

from app import App     # noqa: E402


class TestApp(TestCase):
    """
    The app module test cases.
    """
    def test_constructorPygame(self):
        """
        The constructor must init the pygame package.
        """
        pass
