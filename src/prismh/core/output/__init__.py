#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json

import six

from .common import get_json
from .assessment import Assessment
from .instrument import Instrument


__all__ = (
    'get_instrument_json',
    'get_assessment_json',
)


def _get_struct(src):
    if isinstance(src, six.string_types):
        src = json.loads(src)
    elif hasattr(src, 'read'):
        src = json.load(src)
    return src


def get_instrument_json(instrument, **kwargs):
    instrument = _get_struct(instrument)
    return get_json(Instrument(instrument), **kwargs)


def get_assessment_json(assessment, **kwargs):
    assessment = _get_struct(assessment)
    return get_json(Assessment(assessment), **kwargs)

