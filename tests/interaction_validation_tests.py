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


INSTRUMENT = json.load(open(os.path.join(EXAMPLE_FILES, 'instruments/good/all_interaction_types.json'), 'r'))
INTERACTION = json.load(open(os.path.join(EXAMPLE_FILES, 'interactions/good/all_types.json'), 'r'))


def test_good_instrument_validation():
    validator = Interaction(instrument=INSTRUMENT)
    validator.deserialize(INTERACTION)


def test_bad_instrument_id_reference():
    validator = Interaction(instrument=INSTRUMENT)
    interaction = deepcopy(INTERACTION)
    interaction['instrument']['id'] = 'urn:something-else'
    try:
        validator.deserialize(interaction)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_bad_instrument_version_reference():
    validator = Interaction(instrument=INSTRUMENT)
    interaction = deepcopy(INTERACTION)
    interaction['instrument']['version'] = '2.0'
    try:
        validator.deserialize(interaction)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_missing_field():
    validator = Interaction(instrument=INSTRUMENT)
    interaction = deepcopy(INTERACTION)
    interaction['steps'].pop()
    try:
        validator.deserialize(interaction)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_extra_field():
    validator = Interaction(instrument=INSTRUMENT)
    interaction = deepcopy(INTERACTION)
    interaction['steps'].append({
        'type': 'question',
        'options': {
            'fieldId': 'extra_field',
            'text': {
                'en': 'Extra!'
            }
        }
    })
    try:
        validator.deserialize(interaction)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_duplicate_field():
    validator = Interaction(instrument=INSTRUMENT)
    interaction = deepcopy(INTERACTION)
    interaction['steps'].append(interaction['steps'][1])
    try:
        validator.deserialize(interaction)
    except ValidationError as exc:
        pass
    else:
        assert False

