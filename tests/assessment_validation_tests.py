#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json
import os

from copy import deepcopy

from prismh.core.validation.assessment import Assessment, ValidationError

from utils import EXAMPLE_FILES, check_good_validation, check_bad_validation


GOOD_ASSESSMENT_FILES = os.path.join(EXAMPLE_FILES, 'assessments/good')
BAD_ASSESSMENT_FILES = os.path.join(EXAMPLE_FILES, 'assessments/bad')


def test_good_files():
    for dirpath, dirnames, filenames in os.walk(GOOD_ASSESSMENT_FILES):
        for filename in filenames:
            yield check_good_validation, Assessment(), os.path.join(GOOD_ASSESSMENT_FILES, filename)


def test_bad_files():
    for dirpath, dirnames, filenames in os.walk(BAD_ASSESSMENT_FILES):
        for filename in filenames:
            yield check_bad_validation, Assessment(), os.path.join(BAD_ASSESSMENT_FILES, filename)



INSTRUMENT = json.load(open(os.path.join(EXAMPLE_FILES, 'instruments/good/all_types.json'), 'r'))
ASSESSMENT = json.load(open(os.path.join(EXAMPLE_FILES, 'assessments/good/all_value_types.json'), 'r'))
ASSESSMENT2 = json.load(open(os.path.join(EXAMPLE_FILES, 'assessments/good/all_nulls.json'), 'r'))


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
        pass
    else:
        assert False


def test_bad_instrument_version_reference():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['instrument']['version'] = '2.0'
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_missing_field():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values'].pop('text_field')
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        pass
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
        pass
    else:
        assert False


def test_missing_recordlist_field():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['recordlist_field']['value'][0].pop('subfield1')
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_missing_matrix_row():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['matrix_field']['value'].pop('row2')
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_missing_matrix_column():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['matrix_field']['value']['row2'].pop('col2')
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        pass
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
        pass
    else:
        assert False


def test_required_value():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['boolean_field']['value'] = None
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_undesired_explanation():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['float_field']['explanation'] = 'foo'
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_required_explanation():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    del assessment['values']['integer_field']['explanation']
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_undesired_annotation():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['date_field']['annotation'] = 'foo'
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_undesired_annotation2():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['float_field']['annotation'] = 'foo'
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_required_annotation():
    validator = Assessment(instrument=INSTRUMENT)
    assessment = deepcopy(ASSESSMENT)
    assessment['values']['float_field']['value'] = None
    try:
        validator.deserialize(assessment)
    except ValidationError as exc:
        pass
    else:
        assert False

