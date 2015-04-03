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
    """
    Validates the input against the PRISMH Instrument Definition
    specification.

    :param instrument: The Instrument Definition to validate
    :type instrument: JSON string, dict, or file-like object
    :raises ValidationError: If the input fails any part of the specification
    """

    instrument = _get_struct(instrument)
    validator = Instrument()
    validator.deserialize(instrument)


def validate_assessment(assessment, instrument=None):
    """
    Validates the input against the PRISMH Assessment Document specification.

    :param assessment: The Assessment Document to validate
    :type assessment: JSON string, dict, or file-like object
    :param instrument:
        The Instrument Definition to validate the Assessment against. If not
        specified, this defaults to ``None``, which means that only the basic
        structure of the Assessment will be validated -- not its conformance to
        the Instrument.
    :type instrument: JSON string, dict, or file-like object
    :raises ValidationError: If the input fails any part of the specification
    """

    assessment = _get_struct(assessment)
    if instrument:
        instrument = _get_struct(instrument)
        validate_instrument(instrument)
    validator = Assessment(instrument=instrument)
    validator.deserialize(assessment)

