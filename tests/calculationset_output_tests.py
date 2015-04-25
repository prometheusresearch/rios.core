#
# Copyright (c) 2015, Prometheus Research, LLC
#


from prismh.core.output import get_calculationset_json


CALCULATIONSET = {
    'calculations': [
        {
            'method': 'python',
            'id': 'foo',
            'options': {
                'expression': 'field1 * 2',
            },
            'type': 'integer',
            'description': 'Some description',
        },
        {
            'options': {
                'callable': 'some_module.my_callable',
            },
            'method': 'python',
            'type': 'integer',
            'id': 'bar',
        }
    ],
    'instrument': {
        'version': '1.0',
        'id': 'urn:some-test',
    },
}


EXPECTED = """{
  "instrument": {
    "id": "urn:some-test",
    "version": "1.0"
  },
  "calculations": [
    {
      "id": "foo",
      "description": "Some description",
      "type": "integer",
      "method": "python",
      "options": {
        "expression": "field1 * 2"
      }
    },
    {
      "id": "bar",
      "type": "integer",
      "method": "python",
      "options": {
        "callable": "some_module.my_callable"
      }
    }
  ]
}"""


def test_output_dict():
    actual = get_calculationset_json(CALCULATIONSET, pretty=True)
    assert actual == EXPECTED, actual

