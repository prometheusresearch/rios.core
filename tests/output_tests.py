#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json
import os

import six

from prismh.core.output import *


INSTRUMENT_FILE = os.path.join(os.path.dirname(__file__), 'examples/instruments/good/text.json')

INSTRUMENT_TESTS = (
    open(INSTRUMENT_FILE, 'r'),
    open(INSTRUMENT_FILE, 'r').read(),
    json.load(open(INSTRUMENT_FILE, 'r')),
)

def check_instrument_output(instrument):
    output = get_instrument_json(instrument)
    assert isinstance(output, six.string_types)
    assert len(output) > 0

def test_instrument_output():
    for instrument in INSTRUMENT_TESTS:
        yield check_instrument_output, instrument


CALCULATION_FILE = os.path.join(os.path.dirname(__file__), 'examples/calculationsets/good/text.json')

CALCULATION_TESTS = (
    open(CALCULATION_FILE, 'r'),
    open(CALCULATION_FILE, 'r').read(),
    json.load(open(CALCULATION_FILE, 'r')),
)

def check_calculationset_output(calculationset):
    output = get_calculationset_json(calculationset)
    assert isinstance(output, six.string_types)
    assert len(output) > 0

def test_calculationset_output():
    for calculationset in CALCULATION_TESTS:
        yield check_calculationset_output, calculationset


ASSESSMENT_FILE = os.path.join(os.path.dirname(__file__), 'examples/assessments/good/text.json')

ASSESSMENT_TESTS = (
    open(ASSESSMENT_FILE, 'r'),
    open(ASSESSMENT_FILE, 'r').read(),
    json.load(open(ASSESSMENT_FILE, 'r')),
)

def check_assessment_output(assessment):
    output = get_assessment_json(assessment)
    assert isinstance(output, six.string_types)
    assert len(output) > 0

def test_assessment_output():
    for assessment in ASSESSMENT_TESTS:
        yield check_assessment_output, assessment


FORM_FILE = os.path.join(os.path.dirname(__file__), 'examples/forms/good/text.json')

FORM_TESTS = (
    open(FORM_FILE, 'r'),
    open(FORM_FILE, 'r').read(),
    json.load(open(FORM_FILE, 'r')),
)

def check_form_output(form):
    output = get_form_json(form)
    assert isinstance(output, six.string_types)
    assert len(output) > 0

def test_form_output():
    for form in FORM_TESTS:
        yield check_form_output, form


INTERACTION_FILE = os.path.join(os.path.dirname(__file__), 'examples/interactions/good/text.json')

INTERACTION_TESTS = (
    open(INTERACTION_FILE, 'r'),
    open(INTERACTION_FILE, 'r').read(),
    json.load(open(INTERACTION_FILE, 'r')),
)

def check_interaction_output(interaction):
    output = get_interaction_json(interaction)
    assert isinstance(output, six.string_types)
    assert len(output) > 0

def test_interaction_output():
    for interaction in INTERACTION_TESTS:
        yield check_interaction_output, interaction

