#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json
import os

from copy import deepcopy

from prismh.core.validation.calculationset import CalculationSet, \
    ValidationError

from utils import EXAMPLE_FILES, check_good_validation, check_bad_validation


GOOD_CALCULATION_FILES = os.path.join(EXAMPLE_FILES, 'calculationsets/good')
BAD_CALCULATION_FILES = os.path.join(EXAMPLE_FILES, 'calculationsets/bad')


def test_good_files():
    for dirpath, dirnames, filenames in os.walk(GOOD_CALCULATION_FILES):
        for filename in filenames:
            yield check_good_validation, CalculationSet(), os.path.join(
                GOOD_CALCULATION_FILES,
                filename,
            )


def test_bad_files():
    for dirpath, dirnames, filenames in os.walk(BAD_CALCULATION_FILES):
        for filename in filenames:
            yield check_bad_validation, CalculationSet(), os.path.join(
                BAD_CALCULATION_FILES,
                filename,
            )


INSTRUMENT = json.load(open(os.path.join(EXAMPLE_FILES, 'instruments/good/all_types.json'), 'r'))
CALCULATION = json.load(open(os.path.join(EXAMPLE_FILES, 'calculationsets/good/all_types.json'), 'r'))


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

