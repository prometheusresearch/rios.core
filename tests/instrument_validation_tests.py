#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json
import os

from prismh.core.validation.instrument import Instrument, ValidationError, \
    get_full_type_definition, TYPES_ALL


INSTRUMENT_FILES = os.path.join(os.path.dirname(__file__), 'examples/instruments')
GOOD_INSTRUMENT_FILES = os.path.join(INSTRUMENT_FILES, 'good')
BAD_INSTRUMENT_FILES = os.path.join(INSTRUMENT_FILES, 'bad')


def check_good_file(filename):
    file_contents = open(filename, 'r').read()
    file_structure = json.loads(file_contents)
    validator = Instrument()
    validator.deserialize(file_structure)

def test_good_files():
    for dirpath, dirnames, filenames in os.walk(GOOD_INSTRUMENT_FILES):
        for filename in filenames:
            yield check_good_file, os.path.join(GOOD_INSTRUMENT_FILES, filename)


def check_bad_file(filename):
    file_contents = open(filename, 'r').read()
    file_structure = json.loads(file_contents)
    validator = Instrument()
    try:
        validator.deserialize(file_structure)
    except ValidationError as exc:
        pass
    else:
        assert False, '%s did not fail validation' % filename

def test_bad_files():
    for dirpath, dirnames, filenames in os.walk(BAD_INSTRUMENT_FILES):
        for filename in filenames:
            yield check_bad_file, os.path.join(BAD_INSTRUMENT_FILES, filename)



GFTD_TESTER = {
    'id': 'urn:type-tester',
    'version': '1.0',
    'title': 'A Instrument to Test Types and Inheritance',
    'types': {
        'customText': {
            'base': 'text',
            'pattern': 'foo',
        },
        'customText2': {
            'base': 'customText',
            'length': {
                'min': 2
            },
        },
    },
    'record': [
        {
            'id': 'field1',
            'type': 'text'
        }
    ],
}


def check_gftd_base_type(type_id):
    type_def = get_full_type_definition(GFTD_TESTER, type_id)
    assert isinstance(type_def, dict)
    assert len(type_def.keys()) == 1
    assert type_def['base'] == type_id

def test_gftd_base_id():
    for type_id in TYPES_ALL:
        yield check_gftd_base_type, type_id


def test_gftd_custom_id():
    type_def = get_full_type_definition(GFTD_TESTER, 'customText')
    assert isinstance(type_def, dict)
    assert len(type_def.keys()) == 2
    assert type_def['base'] == 'text'
    assert type_def['pattern'] == 'foo'


def test_gftd_inherited_custom_id():
    type_def = get_full_type_definition(GFTD_TESTER, 'customText2')
    assert isinstance(type_def, dict)
    assert len(type_def.keys()) == 3
    assert type_def['base'] == 'text'
    assert type_def['pattern'] == 'foo'
    assert isinstance(type_def['length'], dict)
    assert len(type_def['length'].keys()) == 1
    assert type_def['length']['min'] == 2


def test_gtfd_custom_def():
    custom_def = {
        'base': 'text',
        'pattern': 'bar',
    }
    type_def = get_full_type_definition(GFTD_TESTER, custom_def)
    assert isinstance(type_def, dict)
    assert len(type_def.keys()) == 2
    assert type_def['base'] == 'text'
    assert type_def['pattern'] == 'bar'


def test_gtfd_inherited_custom_def():
    custom_def = {
        'base': 'customText2',
        'pattern': 'bar',
    }
    type_def = get_full_type_definition(GFTD_TESTER, custom_def)
    assert isinstance(type_def, dict)
    assert len(type_def.keys()) == 3
    assert type_def['base'] == 'text'
    assert type_def['pattern'] == 'bar'
    assert isinstance(type_def['length'], dict)
    assert len(type_def['length'].keys()) == 1
    assert type_def['length']['min'] == 2


def test_gftd_unknown_id():
    try:
        type_def = get_full_type_definition(GFTD_TESTER, 'foobar')
    except ValueError as exc:
        assert 'no type is defined for identifier' in exc.message
    else:
        assert False, 'gftd did not fail, got %r' % type_def


def test_gtfd_unknown_def_base():
    custom_def = {
        'base': 'foobar',
        'pattern': 'bar',
    }
    try:
        type_def = get_full_type_definition(GFTD_TESTER, custom_def)
    except ValueError as exc:
        assert 'references undefined base' in exc.message
    else:
        assert False, 'gftd did not fail, got %r' % type_def


def test_gftd_bad_input():
    try:
        type_def = get_full_type_definition(GFTD_TESTER, False)
    except TypeError as exc:
        assert 'type_def must be a string or dict' in exc.message
    else:
        assert False, 'gftd did not fail, got %r' % type_def

