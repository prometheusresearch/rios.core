#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json
import os

import pytest

from rios.core.validation import *


INSTRUMENT_FILE = os.path.join(os.path.dirname(__file__), 'examples/instruments/good/text.json')
CALCULATION_FILE = os.path.join(os.path.dirname(__file__), 'examples/calculationsets/good/text.json')
ASSESSMENT_FILE = os.path.join(os.path.dirname(__file__), 'examples/assessments/good/text.json')
FORM_FILE = os.path.join(os.path.dirname(__file__), 'examples/forms/good/text.json')
INTERACTION_FILE = os.path.join(os.path.dirname(__file__), 'examples/interactions/good/text.json')



INSTRUMENT_TESTS = (
    open(INSTRUMENT_FILE, 'r'),
    open(INSTRUMENT_FILE, 'r').read(),
    json.load(open(INSTRUMENT_FILE, 'r')),
)

@pytest.mark.parametrize('instrument', INSTRUMENT_TESTS)
def test_instrument_validation(instrument):
    validate_instrument(instrument)


ASSESSMENT_TESTS = (
    (open(ASSESSMENT_FILE, 'r'), None),
    (open(ASSESSMENT_FILE, 'r'), open(INSTRUMENT_FILE, 'r')),
    (open(ASSESSMENT_FILE, 'r'), open(INSTRUMENT_FILE, 'r').read()),
    (open(ASSESSMENT_FILE, 'r'), json.load(open(INSTRUMENT_FILE, 'r'))),

    (open(ASSESSMENT_FILE, 'r').read(), None),
    (open(ASSESSMENT_FILE, 'r').read(), open(INSTRUMENT_FILE, 'r')),
    (open(ASSESSMENT_FILE, 'r').read(), open(INSTRUMENT_FILE, 'r').read()),
    (open(ASSESSMENT_FILE, 'r').read(), json.load(open(INSTRUMENT_FILE, 'r'))),

    (json.load(open(ASSESSMENT_FILE, 'r')), None),
    (json.load(open(ASSESSMENT_FILE, 'r')), open(INSTRUMENT_FILE, 'r')),
    (json.load(open(ASSESSMENT_FILE, 'r')), open(INSTRUMENT_FILE, 'r').read()),
    (json.load(open(ASSESSMENT_FILE, 'r')), json.load(open(INSTRUMENT_FILE, 'r'))),
)

@pytest.mark.parametrize('assessment, instrument', ASSESSMENT_TESTS)
def test_assessment_validation(assessment, instrument):
    validate_assessment(assessment, instrument)


FORM_TESTS = (
    (open(FORM_FILE, 'r'), None),
    (open(FORM_FILE, 'r'), open(INSTRUMENT_FILE, 'r')),
    (open(FORM_FILE, 'r'), open(INSTRUMENT_FILE, 'r').read()),
    (open(FORM_FILE, 'r'), json.load(open(INSTRUMENT_FILE, 'r'))),

    (open(FORM_FILE, 'r').read(), None),
    (open(FORM_FILE, 'r').read(), open(INSTRUMENT_FILE, 'r')),
    (open(FORM_FILE, 'r').read(), open(INSTRUMENT_FILE, 'r').read()),
    (open(FORM_FILE, 'r').read(), json.load(open(INSTRUMENT_FILE, 'r'))),

    (json.load(open(FORM_FILE, 'r')), None),
    (json.load(open(FORM_FILE, 'r')), open(INSTRUMENT_FILE, 'r')),
    (json.load(open(FORM_FILE, 'r')), open(INSTRUMENT_FILE, 'r').read()),
    (json.load(open(FORM_FILE, 'r')), json.load(open(INSTRUMENT_FILE, 'r'))),
)

@pytest.mark.parametrize('form, instrument', FORM_TESTS)
def test_form_validation(form, instrument):
    validate_form(form, instrument)


INTERACTION_TESTS = (
    (open(INTERACTION_FILE, 'r'), None),
    (open(INTERACTION_FILE, 'r'), open(INSTRUMENT_FILE, 'r')),
    (open(INTERACTION_FILE, 'r'), open(INSTRUMENT_FILE, 'r').read()),
    (open(INTERACTION_FILE, 'r'), json.load(open(INSTRUMENT_FILE, 'r'))),

    (open(INTERACTION_FILE, 'r').read(), None),
    (open(INTERACTION_FILE, 'r').read(), open(INSTRUMENT_FILE, 'r')),
    (open(INTERACTION_FILE, 'r').read(), open(INSTRUMENT_FILE, 'r').read()),
    (open(INTERACTION_FILE, 'r').read(), json.load(open(INSTRUMENT_FILE, 'r'))),

    (json.load(open(INTERACTION_FILE, 'r')), None),
    (json.load(open(INTERACTION_FILE, 'r')), open(INSTRUMENT_FILE, 'r')),
    (json.load(open(INTERACTION_FILE, 'r')), open(INSTRUMENT_FILE, 'r').read()),
    (json.load(open(INTERACTION_FILE, 'r')), json.load(open(INSTRUMENT_FILE, 'r'))),
)

@pytest.mark.parametrize('interaction, instrument', INTERACTION_TESTS)
def test_interaction_validation(interaction, instrument):
    validate_interaction(interaction, instrument)


CALCULATION_TESTS = (
    (open(CALCULATION_FILE, 'r'), None),
    (open(CALCULATION_FILE, 'r'), open(INSTRUMENT_FILE, 'r')),
    (open(CALCULATION_FILE, 'r'), open(INSTRUMENT_FILE, 'r').read()),
    (open(CALCULATION_FILE, 'r'), json.load(open(INSTRUMENT_FILE, 'r'))),

    (open(CALCULATION_FILE, 'r').read(), None),
    (open(CALCULATION_FILE, 'r').read(), open(INSTRUMENT_FILE, 'r')),
    (open(CALCULATION_FILE, 'r').read(), open(INSTRUMENT_FILE, 'r').read()),
    (open(CALCULATION_FILE, 'r').read(), json.load(open(INSTRUMENT_FILE, 'r'))),

    (json.load(open(CALCULATION_FILE, 'r')), None),
    (json.load(open(CALCULATION_FILE, 'r')), open(INSTRUMENT_FILE, 'r')),
    (json.load(open(CALCULATION_FILE, 'r')), open(INSTRUMENT_FILE, 'r').read()),
    (json.load(open(CALCULATION_FILE, 'r')), json.load(open(INSTRUMENT_FILE, 'r'))),
)

@pytest.mark.parametrize('calculation, instrument', CALCULATION_TESTS)
def test_calculation_validation(calculation, instrument):
    validate_calculationset(calculation, instrument)

