#
# Copyright (c) 2015, Prometheus Research, LLC
#


from collections import Callable

import colander


__all__ = (
    'ValidationError',
    'sub_schema',
    'AnyType',
    'OneOfType',
    'StrictBooleanType',
    'OptionalStringType',
)


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

