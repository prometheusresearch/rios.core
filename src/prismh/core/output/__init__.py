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


def get_instrument_json(instrument, pretty=True, **kwargs):
    """
    Generates a JSON-formatted string containing the specified Instrument
    Definition.

    :param instrument: The Instrument Definition generate the JSON for
    :type instrument: JSON string, dict, or file-like object
    :param pretty:
        Whether or not to format the JSON in a human-friendly way. If not
        specified, defaults to ``True``.
    :type pretty: bool
    :param kwargs:
        Any extra keyword arguments are passed to the underlying ``json.dumps``
        function.
    :returns: The JSON-formatted string representing the Instrument
    :rtype: string
    """

    instrument = _get_struct(instrument)
    kwargs['pretty'] = pretty
    return get_json(Instrument(instrument), **kwargs)


def get_assessment_json(assessment, pretty=True, **kwargs):
    """
    Generates a JSON-formatted string containing the specified Assessment
    Document.

    :param instrument: The Assessment Document generate the JSON for
    :type instrument: JSON string, dict, or file-like object
    :param pretty:
        Whether or not to format the JSON in a human-friendly way. If not
        specified, defaults to ``True``.
    :type pretty: bool
    :param kwargs:
        Any extra keyword arguments are passed to the underlying ``json.dumps``
        function.
    :returns: The JSON-formatted string representing the Assessment
    :rtype: string
    """

    assessment = _get_struct(assessment)
    kwargs['pretty'] = pretty
    return get_json(Assessment(assessment), **kwargs)

