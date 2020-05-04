#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json
import os

from copy import deepcopy

import pytest

from rios.core.validation.assessment import Assessment, ValidationError

from utils import *


GOOD_ASSESSMENT_FILES = os.path.join(EXAMPLE_FILES, 'assessments/good')
@pytest.mark.parametrize('filename', get_example_files(GOOD_ASSESSMENT_FILES))
def test_good_files(filename):
    check_good_validation(Assessment(), os.path.join(GOOD_ASSESSMENT_FILES, filename))


BAD_ASSESSMENT_FILES = os.path.join(EXAMPLE_FILES, 'assessments/bad')
@pytest.mark.parametrize('filename', get_example_files(BAD_ASSESSMENT_FILES))
def test_bad_files(filename):
    check_bad_validation(Assessment(), os.path.join(BAD_ASSESSMENT_FILES, filename))



INSTRUMENT = json.load(open(os.path.join(EXAMPLE_FILES, 'instruments/good/all_types.json'), 'r'))
ASSESSMENT = json.load(open(os.path.join(EXAMPLE_FILES, 'assessments/good/all_value_types.json'), 'r'))
ASSESSMENT2 = json.load(open(os.path.join(EXAMPLE_FILES, 'assessments/good/all_nulls.json'), 'r'))

CONSTRAINTS_INSTRUMENT = json.load(open(os.path.join(EXAMPLE_FILES, 'instruments/good/constraints.json'), 'r'))
CONSTRAINTS_ASSESSMENT = {
    'instrument': {
        'id': 'urn:example:good:constraints',
        'version': '1.0',
    },
    'values': {
        'field1': {
            'value': None,
        },
    },
}


def test_good_instrument_validation():
    validator = Assessment(instrument=INSTRUMENT)
    validator.deserialize(ASSESSMENT)
    validator.deserialize(ASSESSMENT2)


def test_bad_instrument_id_reference():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['instrument']['id'] = 'urn:something-else'
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'instrument': 'Incorrect Instrument version referenced'},
        )
    else:
        assert False


def test_bad_instrument_version_reference():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['instrument']['version'] = '2.0'
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'instrument': 'Incorrect Instrument version referenced'},
        )
    else:
        assert False


def test_missing_field():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values'].pop('text_field')
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'No value exists for field ID "text_field"'},
        )
    else:
        assert False


def test_extra_field():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['extra_field'] = {
        'value': 42
    }
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'Unknown field IDs found: extra_field'},
        )
    else:
        assert False


def test_missing_recordlist_field():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['recordlist_field']['value'][0].pop('subfield1')
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'No value exists for field ID "subfield1"'},
        )
    else:
        assert False


def test_missing_matrix_row():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['matrix_field']['value'].pop('row2')
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'Missing values for row ID "row2"'},
        )
    else:
        assert False


def test_missing_matrix_column():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['matrix_field']['value']['row2'].pop('col2')
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': u'Row ID "row2" is missing values for columns: col2'},
        )
    else:
        assert False


def test_extra_row():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['matrix_field']['value']['extra_row'] = {
            'col1': {
                'value': 'foo'
            },
            'col2': {
                'value': 'bar'
            }
    }
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'Unknown row IDs found: extra_row'},
        )
    else:
        assert False


def test_extra_column():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['matrix_field']['value']['row2']['fake'] = {'value': 'foo'}
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': u'Row ID "row2" contains unknown column IDs: fake'}
        )
    else:
        assert False


def test_required_row():
    instrument = deepcopy(INSTRUMENT)
    instrument['record'][11]['type']['rows'][0]['required'] = True
    validator = Assessment(instrument=instrument)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['matrix_field']['value']['row1']['col1'] = {'value': None}
    assessment['values']['matrix_field']['value']['row1']['col2'] = {'value': None}
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': u'Row ID "row1" requires at least one column with a value'}
        )
    else:
        assert False


def test_required_column():
    instrument = deepcopy(INSTRUMENT)
    instrument['record'][11]['type']['columns'][0]['required'] = True
    validator = Assessment(instrument=instrument)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['matrix_field']['value']['row1']['col1'] = {'value': None}
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': u'Row ID "row1" is missing values for columns: col1'}
        )
    else:
        assert False

    assessment['values']['matrix_field']['value']['row1']['col1'] = {'value': 'foo'}
    assessment['values']['matrix_field']['value']['row1']['col2'] = {'value': None}
    validator.deserialize(assessment)

def test_required_value():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['boolean_field']['value'] = None
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'No value present for required field ID "boolean_field"'},
        )
    else:
        assert False


def test_undesired_explanation():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['float_field']['explanation'] = 'foo'
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'Explanation present where not allowed in field ID "float_field"'},
        )
    else:
        assert False


def test_required_explanation():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    del assessment['values']['integer_field']['explanation']
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'Explanation missing for field ID "integer_field"'},
        )
    else:
        assert False


def test_undesired_annotation():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['date_field']['annotation'] = 'foo'
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'Annotation present where not allowed: date_field'},
        )
    else:
        assert False


def test_undesired_annotation2():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['float_field']['annotation'] = 'foo'
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'Annotation provided for non-empty value: float_field'},
        )
    else:
        assert False


def test_required_annotation():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['float_field']['value'] = None
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'Annotation missing for field ID "float_field"'},
        )
    else:
        assert False


BAD_VALUE_TESTS = (
    ('text_field', 42, None),
    ('integer_field', 'foo', None),
    ('float_field', 'foo', None),
    ('enumeration_field', False, None),
    ('boolean_field', 42, None),
    ('date_field', '5/22/2015', None),
    ('time_field', 13231123, None),
    ('datetime_field', 'foo', None),
    ('enumerationset_field', 42, None),
    ('enumerationset_field', [{'blah': {'value': None}}], None),
    ('recordlist_field', 42, None),
    ('recordlist_field', [{'subfield1': {'value': 42}, 'subfield2': {'value': 'foo'}}], 'subfield1'),
    ('matrix_field', 'foo', None),
    ('matrix_field', {"row1": {"col1": {"value": False},"col2": {"value": "bar1"}},"row2": {"col1": {"value": "foo2"},"col2": {"value": "bar2"}}}, 'col1'),
)

@pytest.mark.parametrize('field_id, bad_value, sub_field_id', BAD_VALUE_TESTS)
def test_bad_value_types(field_id, bad_value, sub_field_id):
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values'][field_id]['value'] = bad_value
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        msg = 'Value for "%s" is not of the correct type' % (
            sub_field_id or field_id,
        )
        if msg not in str(exc):
            raise
        assert msg in str(exc)
    else:
        assert False


def test_bad_enumeration_choice():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['enumeration_field']['value'] = 'wrong'
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'Value for "enumeration_field" is not an accepted enumeration'},
        )
    else:
        assert False


def test_bad_enumerationset_choice():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['enumerationset_field']['value'] = ['wrong']
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': 'Value for "enumerationset_field" is not an accepted enumeration'},
        )
    else:
        assert False


def test_bad_pattern():
    instrument = deepcopy(CONSTRAINTS_INSTRUMENT)
    instrument['record'][0]['type'] = 'custom_text'
    validator = Assessment(instrument=instrument)
    assessment = deepcopy(CONSTRAINTS_ASSESSMENT)
    assessment['values']['field1']['value'] = 'foo'
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': u'Value for "field1" does not match the specified pattern'},
        )
    else:
        assert False

def test_good_pattern():
    instrument = deepcopy(CONSTRAINTS_INSTRUMENT)
    instrument['record'][0]['type'] = 'custom_text'
    validator = Assessment(instrument=instrument)
    assessment = deepcopy(CONSTRAINTS_ASSESSMENT)
    assessment['values']['field1']['value'] = 'aaa'
    validator.deserialize(assessment)


LENGTH_TESTS = (
    ('custom_text', 'a', 'abcabcabcabc'),
    ('custom_enumerationset', ['foo'], ['foo', 'bar', 'baz', 'blah', 'stuff']),
    (
        'custom_recordlist',
        [{'subfield1': {'value': 'foo'}}],
        [
            {'subfield1': {'value': 'foo'}},
            {'subfield1': {'value': 'foo'}},
            {'subfield1': {'value': 'foo'}},
            {'subfield1': {'value': 'foo'}},
            {'subfield1': {'value': 'foo'}},
        ]
    ),
)

@pytest.mark.parametrize('type_def, short_val, long_val', LENGTH_TESTS)
def test_bad_lengths(type_def, short_val, long_val):
    instrument = deepcopy(CONSTRAINTS_INSTRUMENT)
    instrument['record'][0]['type'] = type_def
    validator = Assessment(instrument=instrument)
    assessment = deepcopy(CONSTRAINTS_ASSESSMENT)
    assessment['values']['field1']['value'] = short_val
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': u'Value for "field1" is less than acceptible minimum length'},
        )
    else:
        assert False

    assessment['values']['field1']['value'] = long_val
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': u'Value for "field1" is greater than acceptible maximum length'},
        )
    else:
        assert False


def test_good_length():
    instrument = deepcopy(CONSTRAINTS_INSTRUMENT)
    instrument['record'][0]['type'] = 'custom_text'
    validator = Assessment(instrument=instrument)
    assessment = deepcopy(CONSTRAINTS_ASSESSMENT)
    assessment['values']['field1']['value'] = 'aaa'
    validator.deserialize(assessment)


RANGE_TESTS = (
    ('custom_integer', 1, 11),
    ('custom_float', 0.23, 11.22),
    ('custom_date', '1999-01-01', '3000-01-01'),
    ('custom_time', '01:01:01', '23:23:23'),
    ('custom_datetime', '1999-01-01T00:00:00', '3000-01-01T12:34:56'),
)

@pytest.mark.parametrize('type_def, small_val, big_val', RANGE_TESTS)
def test_bad_ranges(type_def, small_val, big_val):
    instrument = deepcopy(CONSTRAINTS_INSTRUMENT)
    instrument['record'][0]['type'] = type_def
    validator = Assessment(instrument=instrument)
    assessment = deepcopy(CONSTRAINTS_ASSESSMENT)
    assessment['values']['field1']['value'] = small_val
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': u'Value for "field1" is less than acceptible minimum'},
        )
    else:
        assert False

    assessment['values']['field1']['value'] = big_val
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        assert_validation_error(
            exc,
            {'values': u'Value for "field1" is greater than acceptible maximum'},
        )
    else:
        assert False


def test_good_range():
    instrument = deepcopy(CONSTRAINTS_INSTRUMENT)
    instrument['record'][0]['type'] = 'custom_date'
    validator = Assessment(instrument=instrument)
    assessment = deepcopy(CONSTRAINTS_ASSESSMENT)
    assessment['values']['field1']['value'] = '2012-03-04'
    validator.deserialize(assessment)

