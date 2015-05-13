import json
import os

from prismh.core.validation.common import ValidationError


__all__ = (
    'EXAMPLE_FILES',
    'FAILURES',
    'check_good_validation',
    'check_bad_validation',
)


EXAMPLE_FILES = os.path.join(os.path.dirname(__file__), 'examples')
FAILURES = json.load(open(os.path.join(EXAMPLE_FILES, 'failures.json')))


def check_good_validation(validator, filename):
    file_contents = open(filename, 'r').read()
    file_structure = json.loads(file_contents)
    validator.deserialize(file_structure)


def check_bad_validation(validator, filename):
    file_contents = open(filename, 'r').read()
    file_structure = json.loads(file_contents)
    try:
        validator.deserialize(file_structure)
    except ValidationError as exc:
        filename = os.path.relpath(filename, EXAMPLE_FILES)
        if filename not in FAILURES:
            print filename, exc
        else:
            expected = FAILURES[filename]
            actual = exc.asdict()
            for key, value in expected.items():
                if key in actual:
                    key_actual = actual.pop(key)
                    assert expected[key] == key_actual, 'Expected "%s" to have "%s", got "%s"' % (key, expected[key], key_actual)
                else:
                    assert False, 'Expected failure for "%s"' % (key,)
            if actual:
                assert False, 'Got unexpected failures: "%s"' % (actual,)

    else:
        assert False, '%s did not fail validation' % filename

