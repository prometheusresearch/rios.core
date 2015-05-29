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


def test_duplicate_unprompted_field():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['unprompted']['text_field'] = {
        'action': 'calculate',
        'options': {
            'calculation': '"foo"'
        }
    }
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_unnecessary_enumeration_field():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][0]['elements'][-1]['options']['enumerations'] = [
        {
            'id': 'foo',
            'text': {
                'en': 'Unnecessary'
            }
        }
    ]
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_missing_row():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][1]['elements'][3]['options']['rows'].pop()
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_duplicate_row():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][1]['elements'][3]['options']['rows'][1]['id'] = 'row1'
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_extra_row():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][1]['elements'][3]['options']['rows'].append({
        'id': 'extra',
        'text': {
            'en': 'Extra!',
        },
    })
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_unnecessary_row():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][0]['elements'][-1]['options']['rows'] = [
        {
            'id': 'foo',
            'text': {
                'en': 'Foo'
            }
        }
    ]
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_missing_column():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][1]['elements'][3]['options']['questions'].pop()
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_duplicate_column():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][1]['elements'][3]['options']['questions'][0]['fieldId'] = 'col1'
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_extra_column():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][1]['elements'][3]['options']['questions'].append({
        'fieldId': 'extra',
        'text': {
            'en': 'Extra!',
        },
    })
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_missing_question():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][1]['elements'][2]['options']['questions'].pop()
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_duplicate_question():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][1]['elements'][2]['options']['questions'][0]['fieldId'] = 'col1'
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_extra_question():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][1]['elements'][2]['options']['questions'].append({
        'fieldId': 'extra',
        'text': {
            'en': 'Extra!',
        },
    })
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_unnecessary_question():
    validator = Form(instrument=INSTRUMENT)
    form = deepcopy(FORM)
    form['pages'][0]['elements'][-1]['options']['questions'] = [
        {
            'fieldId': 'foo',
            'text': {
                'en': 'Foo'
            }
        }
    ]
    try:
        validator.deserialize(form)
    except ValidationError as exc:
        pass
    else:
        assert False

