#
# Copyright (c) 2015, Prometheus Research, LLC
#


import re

from collections import Callable

import colander

from six import iteritems


__all__ = (
    'ValidationError',
    'sub_schema',
    'AnyType',
    'OneOfType',
    'StrictBooleanType',
    'OptionalStringType',
    'LanguageTag',
    'LocalizedMapping',
)


# pylint: disable=abstract-method


ValidationError = colander.Invalid


def sub_schema(schema, node, cstruct):
    if not isinstance(schema, colander.SchemaNode):
        schema = schema()
    try:
        schema.deserialize(cstruct)
    except ValidationError as exc:
        exc.node = node
        raise exc


class AnyType(colander.SchemaType):
    # pylint: disable=unused-argument
    def deserialize(self, node, cstruct):
        if cstruct is colander.null:
            return colander.null
        return cstruct


class OneOfType(colander.SchemaType):
    def __init__(self, *args):
        self.possible_types = [
            arg() if isinstance(arg, Callable) else arg
            for arg in args
        ]

    def deserialize(self, node, cstruct):
        for i in range(len(self.possible_types)):
            try:
                return self.possible_types[i].deserialize(node, cstruct)
            except ValidationError:
                if i == (len(self.possible_types) - 1):
                    raise


class StrictBooleanType(colander.SchemaType):
    def deserialize(self, node, cstruct):
        if cstruct is colander.null:
            return colander.null

        if isinstance(cstruct, bool):
            return cstruct

        raise ValidationError(
            node,
            '"%r" is not a boolean value' % (cstruct,)
        )


class OptionalStringType(colander.String):
    def deserialize(self, node, cstruct):
        if cstruct is colander.null or cstruct is None:
            return colander.null

        try:
            result = cstruct
            if isinstance(result, (colander.text_type, bytes)):
                if self.encoding:
                    result = colander.text_(cstruct, self.encoding)
                else:
                    result = colander.text_type(cstruct)
            else:
                raise ValidationError(node)
        except Exception as exc:
            raise ValidationError(
                node,
                colander._(
                    '${val} is not a string: ${err}',
                    mapping={
                        'val': cstruct,
                        'err': exc
                    }
                )
            )

        return result


RE_LANGUAGE_TAG = re.compile(
    r'^(((([A-Za-z]{2,3}(-([A-Za-z]{3}(-[A-Za-z]{3}){0,2}))?)|[A-Za-z]{4}|[A-Za-z]{5,8})(-([A-Za-z]{4}))?(-([A-Za-z]{2}|[0-9]{3}))?(-([A-Za-z0-9]{5,8}|[0-9][A-Za-z0-9]{3}))*(-([0-9A-WY-Za-wy-z](-[A-Za-z0-9]{2,8})+))*(-(x(-[A-Za-z0-9]{1,8})+))?)|(x(-[A-Za-z0-9]{1,8})+)|((en-GB-oed|i-ami|i-bnn|i-default|i-enochian|i-hak|i-klingon|i-lux|i-mingo|i-navajo|i-pwn|i-tao|i-tay|i-tsu|sgn-BE-FR|sgn-BE-NL|sgn-CH-DE)|(art-lojban|cel-gaulish|no-bok|no-nyn|zh-guoyu|zh-hakka|zh-min|zh-min-nan|zh-xiang)))$'  # noqa
)


class LanguageTag(colander.SchemaNode):
    schema_type = colander.String
    validator = colander.Regex(RE_LANGUAGE_TAG)


class LocalizedMapping(colander.SchemaNode):
    def __init__(self, sub_type, *args, **kwargs):
        self.sub_type = sub_type
        kwargs['typ'] = colander.Mapping(unknown='preserve')
        super(LocalizedMapping, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        cstruct = cstruct or {}

        if len(cstruct) == 0:
            raise ValidationError(
                node,
                'At least one localization must be specified',
            )

        for language_tag, translation in iteritems(cstruct):
            sub_schema(LanguageTag, node, language_tag)
            sub_schema(self.sub_type, node, translation)

