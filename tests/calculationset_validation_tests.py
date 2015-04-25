#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json
import os

from copy import deepcopy

from prismh.core.validation.calculationset import CalculationSet, \
    ValidationError


CALCULATION_FILES = os.path.join(
    os.path.dirname(__file__),
    'examples/calculationsets',
)
GOOD_CALCULATION_FILES = os.path.join(CALCULATION_FILES, 'good')
BAD_CALCULATION_FILES = os.path.join(CALCULATION_FILES, 'bad')


def check_good_file(filename):
    file_contents = open(filename, 'r').read()
    file_structure = json.loads(file_contents)
    validator = CalculationSet()
    validator.deserialize(file_structure)

def test_good_files():
    for dirpath, dirnames, filenames in os.walk(GOOD_CALCULATION_FILES):
        for filename in filenames:
            yield check_good_file, os.path.join(
                GOOD_CALCULATION_FILES,
                filename,
            )


def check_bad_file(filename):
    file_contents = open(filename, 'r').read()
    file_structure = json.loads(file_contents)
    validator = CalculationSet()
    try:
        validator.deserialize(file_structure)
    except ValidationError as exc:
        #print os.path.relpath(filename, BAD_CALCULATION_FILES), exc
        pass
    else:
        assert False, '%s did not fail validation' % filename

def test_bad_files():
    for dirpath, dirnames, filenames in os.walk(BAD_CALCULATION_FILES):
        for filename in filenames:
            yield check_bad_file, os.path.join(BAD_CALCULATION_FILES, filename)



INSTRUMENT = json.load(open(os.path.join(os.path.dirname(__file__), 'examples/instruments/good/all_types.json'), 'r'))
CALCULATION = json.load(open(os.path.join(CALCULATION_FILES, 'good/all_types.json'), 'r'))


def test_good_instrument_validation():
    validator = CalculationSet(instrument=INSTRUMENT)
    validator.deserialize(CALCULATION)


def test_bad_instrument_id_reference():
    validator = CalculationSet(instrument=INSTRUMENT)
    calculation = deepcopy(CALCULATION)
    calculation['instrument']['id'] = 'urn:something-else'
    try:
        validator.deserialize(calculation)
    except ValidationError as exc:
        pass
    else:
        assert False


def test_bad_instrument_version_reference():
    validator = CalculationSet(instrument=INSTRUMENT)
    calculation = deepcopy(CALCULATION)
    calculation['instrument']['version'] = '2.0'
    try:
        validator.deserialize(calculation)
    except ValidationError as exc:
        pass
    else:
        assert False

