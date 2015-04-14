#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json

import six

from .common import ValidationError
from .assessment import Assessment
from .form import Form
from .instrument import Instrument


__all__ = (
    'ValidationError',
    'validate_instrument',
    'validate_assessment',
    'validate_form',
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


def validate_form(form, instrument=None):
    """
    Validates the input against the PRISMH Web Form Configuration
    specification.

    :param form: The Web Form Configuration to validate
    :type form: JSON string, dict, or file-like object
    :param instrument:
        The Instrument Definition to validate the FOrm against. If not
        specified, this defaults to ``None``, which means that only the basic
        structure of the Form will be validated -- not its conformance to
        the Instrument.
    :type instrument: JSON string, dict, or file-like object
    :raises ValidationError: If the input fails any part of the specification
    """

    form = _get_struct(form)
    if instrument:
        instrument = _get_struct(instrument)
        validate_instrument(instrument)
    validator = Form(instrument=instrument)
    validator.deserialize(form)

