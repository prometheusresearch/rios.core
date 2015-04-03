#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json

import six

from .common import ValidationError
from .assessment import Assessment
from .instrument import Instrument


__all__ = (
    'ValidationError',
    'validate_instrument',
    'validate_assessment',
)


def _get_struct(src):
    if isinstance(src, six.string_types):
        src = json.loads(src)
    elif hasattr(src, 'read'):
        src = json.load(src)
    return src


def validate_instrument(instrument):
    instrument = _get_struct(instrument)
    validator = Instrument()
    validator.deserialize(instrument)


def validate_assessment(assessment, instrument=None):
    assessment = _get_struct(assessment)
    if instrument:
        instrument = _get_struct(instrument)
        validate_instrument(instrument)
    validator = Assessment(instrument=instrument)
    validator.deserialize(assessment)

