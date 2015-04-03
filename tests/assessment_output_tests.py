#
# Copyright (c) 2015, Prometheus Research, LLC
#


from prismh.core.output import get_assessment_json


ASSESSMENT = {
    'meta': {
        'language': 'en',
        'foo': 'bar',
    },
    'values': {
        'text_field': {
            'explanation': 'Some explanation',
            'annotation': 'Some annotation',
            'value': 'foo',
        },
        'recordlist_field': {
            'value': [
                {
                    'subfield2': {
                        'value': 'bar1',
                    },
                    'subfield1': {
                        'value': 'foo1',
                    },
                },
                {
                    'subfield2': {
                        'value': 'bar2',
                    },
                    'subfield1': {
                        'value': 'foo2',
                    },
                },
            ],
        },
        'integer_field': {
            'meta': {
                'foo': 1,
                'bar': 'baz',
            },
            'value': 42,
        },
        'matrix_field': {
            'value': {
                'row2': {
                    'col2': {
                        'value': 'bar',
                    },
                    'col1': {
                        'value': 'foo',
                    },
                },
                'row1': {
                    'col2': {
                        'explanation': 'Some explanation',
                        'value': 'bar',
                    },
                    'col1': {
                        'value': 'foo',
                    },
                },
            },
        },
    },
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
  "meta": {
    "foo": "bar",
    "language": "en"
  },
  "values": {
    "integer_field": {
      "value": 42,
      "meta": {
        "bar": "baz",
        "foo": 1
      }
    },
    "matrix_field": {
      "value": {
        "row1": {
          "col1": {
            "value": "foo"
          },
          "col2": {
            "value": "bar",
            "explanation": "Some explanation"
          }
        },
        "row2": {
          "col1": {
            "value": "foo"
          },
          "col2": {
            "value": "bar"
          }
        }
      }
    },
    "recordlist_field": {
      "value": [
        {
          "subfield1": {
            "value": "foo1"
          },
          "subfield2": {
            "value": "bar1"
          }
        },
        {
          "subfield1": {
            "value": "foo2"
          },
          "subfield2": {
            "value": "bar2"
          }
        }
      ]
    },
    "text_field": {
      "value": "foo",
      "annotation": "Some annotation",
      "explanation": "Some explanation"
    }
  }
}"""


def test_output_dict():
    actual = get_assessment_json(ASSESSMENT, pretty=True)
    assert actual == EXPECTED, actual

