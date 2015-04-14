#
# Copyright (c) 2015, Prometheus Research, LLC
#


import re

import colander

from six import iteritems

from .common import ValidationError, sub_schema, LanguageTag, LocalizedMapping
from .instrument import InstrumentReference, FieldIdentifier, RE_FIELD_ID


__all__ = (
    'ELEMENT_TYPES_ALL',
    'EVENT_ACTIONS_ALL',
    'UNPROMPTED_ACTIONS_ALL',
    'PARAMETER_TYPES_ALL',
    'RE_PAGE_ID',
    'RE_TAG_ID',
    'RE_PARAMETER_ID',

    'LocalizedString',
    'UrlList',
    'AudioSource',
    'PageIdentifier',
    'TagIdentifier',
    'TagList',
    'ElementType',
    'TextElementOptions',
    'AudioElementOptions',
    'Options',
    'Widget',
    'Descriptor',
    'DescriptorList',
    'Expression',
    'EventAction',
    'EventTarget',
    'EventTargetList',
    'EventList',
    'QuestionList',
    'QuestionElementOptions',
    'Element',
    'ElementList',
    'Page',
    'PageList',
    'UnpromptedAction',
    'UnpromptedOptions',
    'UnpromptedCollection',
    'ParameterType',
    'ParameterIdentifier',
    'ParameterCollection',
    'Form',
)


ELEMENT_TYPES_ALL = (
    'question',
    'header',
    'text',
    'divider',
    'audio',
)


EVENT_ACTIONS_ALL = (
    'hide',
    'disable',
    'hideEnumeration',
    'fail',
    'calculate',
)


UNPROMPTED_ACTIONS_ALL = (
    'calculate',
)


PARAMETER_TYPES_ALL = (
    'text',
    'numeric',
    'boolean',
)


RE_PAGE_ID = re.compile(r'^[a-z](?:[a-z0-9]|[_-](?![_-]))*[a-z0-9]$')
RE_TAG_ID = re.compile(r'^[a-z](?:[a-z0-9]|[_-](?![_-]))*[a-z0-9]$')
RE_PARAMETER_ID = re.compile(r'^[a-zA-Z][a-zA-Z0-9_]*[a-zA-Z0-9]$')


# pylint: disable=abstract-method

class LocalizedString(LocalizedMapping):
    def __init__(self, *args, **kwargs):
        super(LocalizedString, self).__init__(
            colander.SchemaNode(colander.String()),
            *args,
            **kwargs
        )


class UrlList(colander.SequenceSchema):
    url = colander.SchemaNode(colander.String())
    validator = colander.Length(min=1)


class AudioSource(LocalizedMapping):
    def __init__(self, *args, **kwargs):
        super(AudioSource, self).__init__(
            UrlList(),
            *args,
            **kwargs
        )


class PageIdentifier(colander.SchemaNode):
    schema_type = colander.String
    validator = colander.Regex(RE_PAGE_ID)


class TagIdentifier(colander.SchemaNode):
    schema_type = colander.String
    validator = colander.Regex(RE_TAG_ID)


class TagList(colander.SequenceSchema):
    tag = TagIdentifier()
    validator = colander.Length(min=1)


class ElementType(colander.SchemaNode):
    schema_type = colander.String
    validator = colander.OneOf(ELEMENT_TYPES_ALL)


class TextElementOptions(colander.SchemaNode):
    text = LocalizedString()

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(TextElementOptions, self).__init__(*args, **kwargs)


class AudioElementOptions(colander.SchemaNode):
    source = AudioSource()

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(AudioElementOptions, self).__init__(*args, **kwargs)


class Options(colander.SchemaNode):
    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='preserve')
        super(Options, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        cstruct = cstruct or {}
        if len(cstruct) == 0:
            raise ValidationError(
                node,
                'At least one key/value pair must be defined',
            )


class Widget(colander.SchemaNode):
    type = colander.SchemaNode(colander.String())
    options = Options(missing=colander.drop)

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(Widget, self).__init__(*args, **kwargs)


class Descriptor(colander.SchemaNode):
    id = colander.SchemaNode(colander.String())  # pylint: disable=invalid-name
    text = LocalizedString()
    help = LocalizedString(missing=colander.drop)
    audio = AudioSource(missing=colander.drop)

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(Descriptor, self).__init__(*args, **kwargs)


class DescriptorList(colander.SequenceSchema):
    descriptor = Descriptor()
    validator = colander.Length(min=1)


class Expression(colander.SchemaNode):
    schema_type = colander.String


class EventAction(colander.SchemaNode):
    schema_type = colander.String
    validator = colander.OneOf(EVENT_ACTIONS_ALL)


class EventTarget(colander.SchemaNode):
    schema_type = colander.String

    def validator(self, node, cstruct):
        if not RE_PAGE_ID.match(cstruct) \
                and not RE_FIELD_ID.match(cstruct) \
                and not RE_TAG_ID.match(cstruct):
            raise ValidationError(
                node,
                '"%s" is not a valid target identifier' % cstruct,
            )


class EventTargetList(colander.SequenceSchema):
    target = EventTarget()
    validator = colander.Length(min=1)


class Event(colander.SchemaNode):
    trigger = Expression()
    action = EventAction()
    targets = EventTargetList()
    options = Options(missing=colander.drop)

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(Event, self).__init__(*args, **kwargs)


class EventList(colander.SequenceSchema):
    event = Event()
    validator = colander.Length(min=1)


class QuestionList(colander.SchemaNode):
    validator = colander.Length(min=1)

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Sequence()
        super(QuestionList, self).__init__(*args, **kwargs)
        self.add(QuestionElementOptions(
            allow_complex=False,
            name='question',
        ))


class QuestionElementOptions(colander.SchemaNode):
    fieldId = FieldIdentifier()
    text = LocalizedString()
    audio = AudioSource(missing=colander.drop)
    help = LocalizedString(missing=colander.drop)
    error = LocalizedString(missing=colander.drop)
    enumerations = DescriptorList(missing=colander.drop)
    widget = Widget(missing=colander.drop)
    events = EventList(missing=colander.drop)

    def __init__(self, *args, **kwargs):
        self.allow_complex = kwargs.pop('allow_complex', True)
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(QuestionElementOptions, self).__init__(*args, **kwargs)
        if self.allow_complex:
            self.add(QuestionList(
                name='questions',
                missing=colander.drop,
            ))
            self.add(DescriptorList(
                name='rows',
                missing=colander.drop,
            ))


ELEMENT_TYPE_OPTION_VALIDATORS = {
    'question': QuestionElementOptions(),
    'text': TextElementOptions(),
    'header': TextElementOptions(),
    'audio': AudioElementOptions(),
}


class Element(colander.SchemaNode):
    type = ElementType()
    options = Options(missing=colander.drop)
    tags = TagList(missing=colander.drop)

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(Element, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        element_type = cstruct.get('type', None)
        validator = ELEMENT_TYPE_OPTION_VALIDATORS.get(element_type, None)
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
                '"%s" elements do not accept options' % element_type,
            )


class ElementList(colander.SequenceSchema):
    element = Element()
    validator = colander.Length(min=1)


class Page(colander.SchemaNode):
    id = PageIdentifier()  # pylint: disable=invalid-name
    elements = ElementList()

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(Page, self).__init__(*args, **kwargs)


class PageList(colander.SequenceSchema):
    page = Page()

    def validator(self, node, cstruct):
        if len(cstruct) < 1:
            raise ValidationError(
                node,
                'Shorter than minimum length 1',
            )

        ids = [page['id'] for page in cstruct]
        if len(ids) != len(set(ids)):
            raise ValidationError(
                node,
                'Page IDs must be unique',
            )


class UnpromptedAction(colander.SchemaNode):
    schema_type = colander.String
    validator = colander.OneOf(UNPROMPTED_ACTIONS_ALL)


class UnpromptedOptions(colander.SchemaNode):
    action = UnpromptedAction()
    options = Options(missing=colander.drop)

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(UnpromptedOptions, self).__init__(*args, **kwargs)


class UnpromptedCollection(colander.SchemaNode):
    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='preserve')
        super(UnpromptedCollection, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        cstruct = cstruct or {}
        if len(cstruct) == 0:
            raise ValidationError(
                node,
                'At least one key/value pair must be defined',
            )

        for name, options in iteritems(cstruct):
            sub_schema(FieldIdentifier, node, name)
            sub_schema(UnpromptedOptions, node, options)


class ParameterType(colander.SchemaNode):
    schema_type = colander.String
    validator = colander.OneOf(PARAMETER_TYPES_ALL)


class ParameterOptions(colander.SchemaNode):
    type = ParameterType()

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(ParameterOptions, self).__init__(*args, **kwargs)


class ParameterIdentifier(colander.SchemaNode):
    schema_type = colander.String
    validator = colander.Regex(RE_PARAMETER_ID)


class ParameterCollection(colander.SchemaNode):
    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='preserve')
        super(ParameterCollection, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        cstruct = cstruct or {}
        if len(cstruct) == 0:
            raise ValidationError(
                node,
                'At least one key/value pair must be defined',
            )

        for name, options in iteritems(cstruct):
            sub_schema(ParameterIdentifier, node, name)
            sub_schema(ParameterOptions, node, options)


class Form(colander.SchemaNode):
    instrument = InstrumentReference()
    defaultLocalization = LanguageTag()
    title = LocalizedString(missing=colander.drop)
    pages = PageList()
    unprompted = UnpromptedCollection(missing=colander.drop)
    parameters = ParameterCollection(missing=colander.drop)

    def __init__(self, instrument=None, *args, **kwargs):
        self.instrument = instrument
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(Form, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        # TODO make sure all localizable strings have the default localization

        # TODO check for duplicated field IDs

        if not self.instrument:
            return

        if self.instrument['id'] != cstruct['instrument']['id'] or \
                self.instrument['version'] != cstruct['instrument']['version']:
            raise ValidationError(
                node.get('instrument'),
                'Form does not reference the specified version',
            )

        # TODO make sure all fields, columns, rows, and subfields are addressed

        # TODO make sure enumeration config is appropriate for type
