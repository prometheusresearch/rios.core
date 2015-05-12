#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json
import os

from copy import deepcopy

from prismh.core.validation.interaction import Interaction, ValidationError


INTERACTION_FILES = os.path.join(os.path.dirname(__file__), 'examples/interactions')
GOOD_INTERACTION_FILES = os.path.join(INTERACTION_FILES, 'good')
BAD_INTERACTION_FILES = os.path.join(INTERACTION_FILES, 'bad')


def check_good_file(filename):
    file_contents = open(filename, 'r').read()
    file_structure = json.loads(file_contents)
    validator = Interaction()
    validator.deserialize(file_structure)

def test_good_files():
    for dirpath, dirnames, filenames in os.walk(GOOD_INTERACTION_FILES):
        for filename in filenames:
            yield check_good_file, os.path.join(GOOD_INTERACTION_FILES, filename)


def check_bad_file(filename):
    file_contents = open(filename, 'r').read()
    file_structure = json.loads(file_contents)
    validator = Interaction()
    try:
        validator.deserialize(file_structure)
    except ValidationError as exc:
        print os.path.relpath(filename, BAD_INTERACTION_FILES), exc
        pass
    else:
        assert False, '%s did not fail validation' % filename

def test_bad_files():
    for dirpath, dirnames, filenames in os.walk(BAD_INTERACTION_FILES):
        for filename in filenames:
            yield check_bad_file, os.path.join(BAD_INTERACTION_FILES, filename)

