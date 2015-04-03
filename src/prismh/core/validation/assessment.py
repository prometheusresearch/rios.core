#
# Copyright (c) 2015, Prometheus Research, LLC
#


import re

from copy import deepcopy

import colander

from six import iteritems

from .common import ValidationError, sub_schema, AnyType
from .instrument import InstrumentReference, RE_FIELD_ID, \
    get_full_type_definition


__all__ = (
    'METADATA_SCOPE_ASSESSMENT',
    'METADATA_SCOPE_VALUE',
    'METADATA_STANDARD_PROPERTIES',
    'RE_LANGUAGE_TAG',

    'MetadataCollection',
    'ValueCollection',
    'Assessment',
)


RE_LANGUAGE_TAG = re.compile(
    r'^(((([A-Za-z]{2,3}(-([A-Za-z]{3}(-[A-Za-z]{3}){0,2}))?)|[A-Za-z]{4}|[A-Za-z]{5,8})(-([A-Za-z]{4}))?(-([A-Za-z]{2}|[0-9]{3}))?(-([A-Za-z0-9]{5,8}|[0-9][A-Za-z0-9]{3}))*(-([0-9A-WY-Za-wy-z](-[A-Za-z0-9]{2,8})+))*(-(x(-[A-Za-z0-9]{1,8})+))?)|(x(-[A-Za-z0-9]{1,8})+)|((en-GB-oed|i-ami|i-bnn|i-default|i-enochian|i-hak|i-klingon|i-lux|i-mingo|i-navajo|i-pwn|i-tao|i-tay|i-tsu|sgn-BE-FR|sgn-BE-NL|sgn-CH-DE)|(art-lojban|cel-gaulish|no-bok|no-nyn|zh-guoyu|zh-hakka|zh-min|zh-min-nan|zh-xiang)))$'  # noqa
)
RE_PRODUCT_TOKEN = re.compile(r'^(.+)/(.+)$')


METADATA_SCOPE_ASSESSMENT = 'assessment'
METADATA_SCOPE_VALUE = 'value'

METADATA_STANDARD_PROPERTIES = {
    METADATA_SCOPE_ASSESSMENT: {
        'language': colander.SchemaNode(
            colander.String(),
            validator=colander.Regex(RE_LANGUAGE_TAG),
        ),
        'application': colander.SchemaNode(
            colander.String(),
            validator=colander.Regex(RE_PRODUCT_TOKEN),
        ),
        'dateCompleted': colander.SchemaNode(
            colander.DateTime(),
        ),
        'timeTaken': colander.SchemaNode(
            colander.Integer(),
        ),
    },

    METADATA_SCOPE_VALUE: {
        'timeTaken': colander.SchemaNode(
            colander.Integer(),
        ),
    },
}


# pylint: disable=abstract-method


class MetadataCollection(colander.SchemaNode):
    def __init__(self, scope, *args, **kwargs):
        self.scope = scope
        kwargs['typ'] = colander.Mapping(unknown='preserve')
        super(MetadataCollection, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        cstruct = cstruct or {}
        if len(cstruct) == 0:
            raise ValidationError(
                node,
                'At least one propety must be defined',
            )

        standards = METADATA_STANDARD_PROPERTIES.get(self.scope, {})

        for prop, value in iteritems(cstruct):
            if prop in standards:
                sub_schema(standards[prop], node, value)


class Value(colander.SchemaNode):
    value = colander.SchemaNode(
        AnyType(),
    )
    explanation = colander.SchemaNode(
        colander.String(),
        missing=colander.drop,
    )
    annotation = colander.SchemaNode(
        colander.String(),
        missing=colander.drop,
    )
    meta = MetadataCollection(
        METADATA_SCOPE_VALUE,
        missing=colander.drop,
    )

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(Value, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        if isinstance(cstruct['value'], list):
            for subtype in (
                    colander.SchemaNode(colander.String()),
                    ValueCollection):
                for value in cstruct['value']:
                    try:
                        sub_schema(subtype, node, value)
                    except ValidationError:
                        break
                else:
                    return

            raise ValidationError(
                node,
                'Lists must be consist only of Strings or ValueCollections',
            )

        elif isinstance(cstruct['value'], dict):
            sub_schema(ValueCollectionMapping, node, cstruct['value'])


class ValueCollection(colander.SchemaNode):
    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='preserve')
        super(ValueCollection, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        cstruct = cstruct or {}
        if len(cstruct) == 0:
            raise ValidationError(
                node,
                'At least one Value must be defined',
            )

        for field_id, value in iteritems(cstruct):
            if not RE_FIELD_ID.match(field_id):
                raise ValidationError(
                    node,
                    '"%r" is not a valid Field ID' % field_id,
                )
            sub_schema(Value, node, value)


class ValueCollectionMapping(colander.SchemaNode):
    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='preserve')
        super(ValueCollectionMapping, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        cstruct = cstruct or {}
        if len(cstruct) == 0:
            raise ValidationError(
                node,
                'At least one Row must be defined',
            )

        for field_id, values in iteritems(cstruct):
            if not RE_FIELD_ID.match(field_id):
                raise ValidationError(
                    node,
                    '"%r" is not a valid Field ID' % field_id,
                )
            sub_schema(ValueCollection, node, values)


class Assessment(colander.SchemaNode):
    instrument = InstrumentReference()
    meta = MetadataCollection(
        METADATA_SCOPE_ASSESSMENT,
        missing=colander.drop,
    )
    values = ValueCollection()

    def __init__(self, instrument=None, *args, **kwargs):
        self.instrument = instrument
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(Assessment, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        if not self.instrument:
            return

        if self.instrument['id'] != cstruct['instrument']['id'] or \
                self.instrument['version'] != cstruct['instrument']['version']:
            raise ValidationError(
                node.get('instrument'),
                'Assessment does not reference the specified version',
            )

        self.check_has_all_fields(
            node.get('values'),
            cstruct['values'],
            self.instrument['record'],
        )

    def check_has_all_fields(self, node, values, fields):
        values = deepcopy(values)

        for field in fields:
            value = values.pop(field['id'], None)
            if value is None:
                raise ValidationError(
                    node,
                    'No value exists for field ID "%s"' % field['id'],
                )

            full_type_def = get_full_type_definition(
                self.instrument,
                field['type'],
            )

            # TODO check value type

            self._check_metafields(node, value, field)
            self._check_complex_subfields(node, full_type_def, value)

        if len(values) > 0:
            raise ValidationError(
                node,
                'Unknown field IDs found: %s' % ', '.join(values.keys()),
            )

    def _check_metafields(self, node, value, field):
        explanation = field.get('explanation', 'none')
        if 'explanation' in value and explanation == 'none':
            raise ValidationError(
                node,
                'Explanation present where not allowed',
            )

        annotation = field.get('annotation', 'none')
        if 'annotation' in value:
            if annotation == 'none':
                raise ValidationError(
                    node,
                    'Annotation present where not allowed',
                )

            elif value['value'] is not None:
                raise ValidationError(
                    node,
                    'Annotation provided for non-empty value',
                )

    def _check_complex_subfields(self, node, full_type_def, value):
        if 'record' in full_type_def:
            for rec in value['value']:
                self.check_has_all_fields(
                    node,
                    rec,
                    full_type_def['record'],
                )

        elif 'rows' in full_type_def:
            for row in full_type_def['rows']:
                row_value = value['value'].pop(row['id'], None)
                if row_value is None:
                    raise ValidationError(
                        node,
                        'Missing values for row ID "%s"' % row['id'],
                    )

                self.check_has_all_fields(
                    node,
                    row_value,
                    full_type_def['columns'],
                )

            if len(value['value']) > 0:
                raise ValidationError(
                    node,
                    'Unknown row IDs found: %s' % (
                        ', '.join(value['value'].keys()),
                    ),
                )

