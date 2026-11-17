"""Hooks for behave.

before_scenario runs automatically before every scenario, so each scenario
starts with a fresh, empty ParkEase object. This set-up is a technical detail,
so it lives here and not in the Gherkin text.
"""

import os
import sys

# Make "import parkease" work when behave is started from the project folder.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parkease import ParkEase  # noqa: E402


def before_scenario(context, scenario):
    context.app = ParkEase()
    context.plate = None
    context.minutes = 0
    context.seconds = 0
    context.result = None
