#
# Copyright (c) 2015, Prometheus Research, LLC
#


import colander

from .common import ValidationError, sub_schema, Options
from .instrument import InstrumentReference, IdentifierString, Description, \
    TYPES_SIMPLE


__all__ = (
    'METHODS_ALL',

    'CalculationResultType',
    'CalculationMethod',
    'Expression',
    'PythonOptions',
    'HtsqlOptions',
    'Calculation',
    'CalculationList',
    'CalculationSet',
)


METHODS_ALL = (
    'python',
    'htsql',
)


# pylint: disable=abstract-method


class CalculationResultType(colander.SchemaNode):
    schema_type = colander.String
    validator = colander.OneOf(TYPES_SIMPLE)


class CalculationMethod(colander.SchemaNode):
    schema_type = colander.String
    validator = colander.OneOf(METHODS_ALL)


class Expression(colander.SchemaNode):
    schema_type = colander.String


class PythonOptions(colander.SchemaNode):
    expression = Expression(missing=colander.drop)
    callable = Expression(missing=colander.drop)

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(PythonOptions, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        if ('expression' in cstruct) == ('callable' in cstruct):
            raise ValidationError(
                node,
                'Exactly one option of "exression" or "callable" must be'
                ' specified',
            )


class HtsqlOptions(colander.SchemaNode):
    expression = Expression()

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(HtsqlOptions, self).__init__(*args, **kwargs)


METHOD_OPTION_VALIDATORS = {
    'python': PythonOptions(),
    'htsql': HtsqlOptions(),
}


class Calculation(colander.SchemaNode):
    id = IdentifierString()  # pylint: disable=invalid-name
    description = Description()
    type = CalculationResultType()
    method = CalculationMethod()
    options = Options(missing=colander.drop)

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(Calculation, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        method = cstruct.get('method', None)
        validator = METHOD_OPTION_VALIDATORS.get(method, None)
        options = cstruct.get('options', None)
        if validator:
            sub_schema(
                validator,
                node.get('options'),
                options,
            )
        elif options is not None:
            raise ValidationError(
                node.get('options'),
                'The "%s" method does not accept options' % method,
            )


class CalculationList(colander.SequenceSchema):
    calculation = Calculation()

    def validator(self, node, cstruct):
        if len(cstruct) < 1:
            raise ValidationError(
                node,
                'Shorter than minimum length 1',
            )

        ids = [calculation['id'] for calculation in cstruct]
        if len(ids) != len(set(ids)):
            raise ValidationError(
                node,
                'Calculation IDs must be unique',
            )


class CalculationSet(colander.SchemaNode):
    instrument = InstrumentReference()
    calculations = CalculationList()

    def __init__(self, instrument=None, *args, **kwargs):
        self.instrument = instrument
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(CalculationSet, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        if not self.instrument:
            return

        if self.instrument['id'] != cstruct['instrument']['id'] or \
                self.instrument['version'] != cstruct['instrument']['version']:
            raise ValidationError(
                node.get('instrument'),
                'CalculationSet does not reference the specified version',
            )

