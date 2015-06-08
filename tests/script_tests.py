#
# Copyright (c) 2015, Prometheus Research, LLC
#


from six import StringIO

from prismh.core.scripts import validate


def run_validate(args, expected, exit=0):
    actual = StringIO()
    actual_exit = validate(args, stdout=actual)
    assert actual.getvalue().strip() == expected, actual.getvalue()
    assert actual_exit == exit, actual_exit


def test_validate_good_instrument():
    run_validate(
        ['instrument', 'tests/examples/instruments/good/all_types.json'],
        'tests/examples/instruments/good/all_types.json successfully validated.',
    )


def test_validate_bad_instrument():
    run_validate(
        ['instrument', 'tests/examples/instruments/bad/title_missing.json'],
        'tests/examples/instruments/bad/title_missing.json failed validation.\ntitle: Required',
        exit=1,
    )


def test_validate_form():
    run_validate(
        ['form', 'tests/examples/forms/good/all_types.json'],
        'tests/examples/forms/good/all_types.json successfully validated.',
    )


def test_validate_form_with_instrument():
    run_validate(
        ['form', 'tests/examples/forms/good/all_types.json', '-i', 'tests/examples/instruments/good/all_types.json'],
        'tests/examples/forms/good/all_types.json successfully validated.',
    )

