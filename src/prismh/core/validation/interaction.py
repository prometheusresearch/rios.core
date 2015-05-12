#
# Copyright (c) 2015, Prometheus Research, LLC
#


import colander

from six import iteritems

from .common import ValidationError, sub_schema, LanguageTag, \
    LocalizedMapping, IdentifierString, Options, LocalizedString, Descriptor, \
    DescriptorList
from .instrument import InstrumentReference


__all__ = (
    'Interaction',
)


STEP_TYPES_ALL = (
    'question',
    'text',
)


class StepType(colander.SchemaNode):
    schema_type = colander.String
    validator = colander.OneOf(STEP_TYPES_ALL)


class TextStepOptions(colander.SchemaNode):
    text = LocalizedString()

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(TextStepOptions, self).__init__(*args, **kwargs)


class QuestionStepOptions(colander.SchemaNode):
    fieldId = IdentifierString()
    text = LocalizedString()
    error = LocalizedString(missing=colander.drop)
    enumerations = DescriptorList(missing=colander.drop)

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(QuestionStepOptions, self).__init__(*args, **kwargs)


STEP_TYPE_OPTION_VALIDATORS = {
    'question': QuestionStepOptions(),
    'text': TextStepOptions(),
}


class Step(colander.SchemaNode):
    type = StepType()
    options = Options(missing=colander.drop)

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(Step, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        step_type = cstruct.get('type', None)
        validator = STEP_TYPE_OPTION_VALIDATORS.get(step_type, None)
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
                '"%s" step do not accept options' % step_type,
            )


class StepList(colander.SequenceSchema):
    step = Step()
    validator = colander.Length(min=1)


class Threshold(colander.SchemaNode):
    schema_type = colander.Integer
    validator = colander.Range(min=1)


class TimeoutDetails(colander.SchemaNode):
    threshold = Threshold()
    text = LocalizedString()

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(TimeoutDetails, self).__init__(*args, **kwargs)


class Timeout(colander.SchemaNode):
    warn = TimeoutDetails(missing=colander.drop)
    abort = TimeoutDetails(missing=colander.drop)

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(Timeout, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        if not cstruct.get('warn') and not cstruct.get('abort'):
            raise ValidationError(
                node,
                'At least one of "warn" or "abort" must be defined',
            )


class Interaction(colander.SchemaNode):
    instrument = InstrumentReference()
    defaultLocalization = LanguageTag()
    defaultTimeout = Timeout(missing=colander.drop)
    steps = StepList()

    def __init__(self, instrument=None, *args, **kwargs):
        self.instrument = instrument
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(Interaction, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        # TODO make sure all localizable strings have the default localization

        # TODO check for duplicated field IDs

        if not self.instrument:
            return

        if self.instrument['id'] != cstruct['instrument']['id'] or \
                self.instrument['version'] != cstruct['instrument']['version']:
            raise ValidationError(
                node.get('instrument'),
                'Interaction does not reference the specified version',
            )

        # TODO make sure all fields are addressed

        # TODO make sure enumeration config is appropriate for type

        # TODO make sure no recordList or matrix field types

