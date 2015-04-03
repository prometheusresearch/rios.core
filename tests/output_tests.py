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

