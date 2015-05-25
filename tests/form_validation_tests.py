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


INSTRUMENT = json.load(open(os.path.join(EXAMPLE_FILES, 'instruments/good/all_types.json'), 'r'))
FORM = json.load(open(os.path.join(EXAMPLE_FILES, 'forms/good/all_types.json'), 'r'))


def test_good_instrument_validation():
    validator = Form(instrument=INSTRUMENT)
    validator.deserialize(FORM)


def test_bad_instrument_id_reference():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['instrument']['id'] = 'urn:something-else'
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_bad_instrument_version_reference():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['instrument']['version'] = '2.0'
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_missing_field():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][0]['elements'].pop()
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_extra_field():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][0]['elements'].append({
        'type': 'question',
        'options': {
            'fieldId': 'extra_field',
            'text': {
                'en': 'Extra!'
            }
        }
    })
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_duplicate_field():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][0]['elements'].append(form['pages'][0]['elements'][-1])
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        pass
    else:
        assert False

