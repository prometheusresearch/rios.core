#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json
import os

from prismh.core.validation import *


INSTRUMENT_FILE = os.path.join(os.path.dirname(__file__), 'examples/instruments/good/text.json')
ASSESSMENT_FILE = os.path.join(os.path.dirname(__file__), 'examples/assessments/good/text.json')



INSTRUMENT_TESTS = (
    open(INSTRUMENT_FILE, 'r'),
    open(INSTRUMENT_FILE, 'r').read(),
    json.load(open(INSTRUMENT_FILE, 'r')),
)

def test_instrument_validation():
    for instrument in INSTRUMENT_TESTS:
        yield validate_instrument, instrument


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

def test_assessment_validation():
    for assessment, instrument in ASSESSMENT_TESTS:
        yield validate_assessment, assessment, instrument

