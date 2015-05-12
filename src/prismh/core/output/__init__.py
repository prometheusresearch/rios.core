#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json

import six

from .common import get_json
from .assessment import Assessment
from .calculationset import CalculationSet
from .form import Form
from .instrument import Instrument
from .interaction import Interaction


__all__ = (
    'get_instrument_json',
    'get_assessment_json',
    'get_form_json',
    'get_calculationset_json',
    'get_interaction_json',
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


def get_form_json(form, pretty=True, **kwargs):
    """
    Generates a JSON-formatted string containing the specified Web Form
    Configuration.

    :param instrument: The Web Form Configuration generate the JSON for
    :type instrument: JSON string, dict, or file-like object
    :param pretty:
        Whether or not to format the JSON in a human-friendly way. If not
        specified, defaults to ``True``.
    :type pretty: bool
    :param kwargs:
        Any extra keyword arguments are passed to the underlying ``json.dumps``
        function.
    :returns: The JSON-formatted string representing the Form
    :rtype: string
    """

    form = _get_struct(form)
    kwargs['pretty'] = pretty
    return get_json(Form(form), **kwargs)


def get_calculationset_json(calculationset, pretty=True, **kwargs):
    """
    Generates a JSON-formatted string containing the specified Calculation Set
    Definition.

    :param instrument: The Calculation Set Definition generate the JSON for
    :type instrument: JSON string, dict, or file-like object
    :param pretty:
        Whether or not to format the JSON in a human-friendly way. If not
        specified, defaults to ``True``.
    :type pretty: bool
    :param kwargs:
        Any extra keyword arguments are passed to the underlying ``json.dumps``
        function.
    :returns: The JSON-formatted string representing the Calculation Set
    :rtype: string
    """

    calculationset = _get_struct(calculationset)
    kwargs['pretty'] = pretty
    return get_json(CalculationSet(calculationset), **kwargs)


def get_interaction_json(interaction, pretty=True, **kwargs):
    """
    Generates a JSON-formatted string containing the specified SMS Interaction
    Configuration.

    :param instrument: The SMS Interaction Configuration generate the JSON for
    :type instrument: JSON string, dict, or file-like object
    :param pretty:
        Whether or not to format the JSON in a human-friendly way. If not
        specified, defaults to ``True``.
    :type pretty: bool
    :param kwargs:
        Any extra keyword arguments are passed to the underlying ``json.dumps``
        function.
    :returns: The JSON-formatted string representing the Form
    :rtype: string
    """

    interaction = _get_struct(interaction)
    kwargs['pretty'] = pretty
    return get_json(Interaction(interaction), **kwargs)

