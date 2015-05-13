#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json
import os

from copy import deepcopy

from prismh.core.validation.interaction import Interaction, ValidationError

from utils import EXAMPLE_FILES, check_good_validation, check_bad_validation


GOOD_INTERACTION_FILES = os.path.join(EXAMPLE_FILES, 'interactions/good')
BAD_INTERACTION_FILES = os.path.join(EXAMPLE_FILES, 'interactions/bad')


def test_good_files():
    for dirpath, dirnames, filenames in os.walk(GOOD_INTERACTION_FILES):
        for filename in filenames:
            yield check_good_validation, Interaction(), os.path.join(
                GOOD_INTERACTION_FILES,
                filename,
            )


def test_bad_files():
    for dirpath, dirnames, filenames in os.walk(BAD_INTERACTION_FILES):
        for filename in filenames:
            yield check_bad_validation, Interaction(), os.path.join(
                BAD_INTERACTION_FILES,
                filename,
            )

