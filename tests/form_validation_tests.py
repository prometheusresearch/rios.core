#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json
import os

from copy import deepcopy

from prismh.core.validation.form import Form, ValidationError


FORM_FILES = os.path.join(os.path.dirname(__file__), 'examples/forms')
GOOD_FORM_FILES = os.path.join(FORM_FILES, 'good')
BAD_FORM_FILES = os.path.join(FORM_FILES, 'bad')


def check_good_file(filename):
    file_contents = open(filename, 'r').read()
    file_structure = json.loads(file_contents)
    validator = Form()
    validator.deserialize(file_structure)

def test_good_files():
    for dirpath, dirnames, filenames in os.walk(GOOD_FORM_FILES):
        for filename in filenames:
            yield check_good_file, os.path.join(GOOD_FORM_FILES, filename)


def check_bad_file(filename):
    file_contents = open(filename, 'r').read()
    file_structure = json.loads(file_contents)
    validator = Form()
    try:
        validator.deserialize(file_structure)
    except ValidationError as exc:
        pass
    else:
        assert False, '%s did not fail validation' % filename

def test_bad_files():
    for dirpath, dirnames, filenames in os.walk(BAD_FORM_FILES):
        for filename in filenames:
            yield check_bad_file, os.path.join(BAD_FORM_FILES, filename)

