#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json
import os

from copy import deepcopy

from prismh.core.validation.form import Form, ValidationError

from utils import EXAMPLE_FILES, check_good_validation, check_bad_validation


GOOD_FORM_FILES = os.path.join(EXAMPLE_FILES, 'forms/good')
BAD_FORM_FILES = os.path.join(EXAMPLE_FILES, 'forms/bad')


def test_good_files():
    for dirpath, dirnames, filenames in os.walk(GOOD_FORM_FILES):
        for filename in filenames:
            yield check_good_validation, Form(), os.path.join(GOOD_FORM_FILES, filename)


def test_bad_files():
    for dirpath, dirnames, filenames in os.walk(BAD_FORM_FILES):
        for filename in filenames:
            yield check_bad_validation, Form(), os.path.join(BAD_FORM_FILES, filename)

