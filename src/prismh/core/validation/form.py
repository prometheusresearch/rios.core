#
# Copyright (c) 2015, Prometheus Research, LLC
#


import colander

from six import iteritems, iterkeys

from .common import ValidationError, sub_schema, LanguageTag, \
    LocalizedMapping, IdentifierString, Options, LocalizedString, \
    Descriptor as BaseDescriptor, LocalizationChecker, \
    validate_instrument_version, CompoundIdentifierString
from .instrument import InstrumentReference, get_full_type_definition


__all__ = (
    'ELEMENT_TYPES_ALL',
    'EVENT_ACTIONS_ALL',
    'UNPROMPTED_ACTIONS_ALL',
    'PARAMETER_TYPES_ALL',

    'Descriptor',
    'DescriptorList',
    'UrlList',
    'AudioSource',
    'TagList',
    'ElementType',
    'TextElementOptions',
    'AudioElementOptions',
    'Options',
    'Widget',
    'Expression',
    'EventAction',
    'EventTargetList',
    'EventList',
    'QuestionList',
    'QuestionElementOptions',
    'Element',
    'ElementList',
    'Page',
    'PageList',
    'UnpromptedAction',
    'CalculateUnpromptedOptions',
    'Unprompted',
    'UnpromptedCollection',
    'ParameterType',
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


# pylint: disable=abstract-method


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


class TagList(colander.SequenceSchema):
    tag = IdentifierString()
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


class Widget(colander.SchemaNode):
    type = colander.SchemaNode(colander.String())
    options = Options(missing=colander.drop)

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(Widget, self).__init__(*args, **kwargs)


class Expression(colander.SchemaNode):
    schema_type = colander.String


class EventAction(colander.SchemaNode):
    schema_type = colander.String
    validator = colander.OneOf(EVENT_ACTIONS_ALL)


class EventTargetList(colander.SequenceSchema):
    target = CompoundIdentifierString()
    validator = colander.Length(min=1)


class Event(colander.SchemaNode):
    trigger = Expression()
    action = EventAction()
    targets = EventTargetList(missing=colander.drop)
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


class Descriptor(BaseDescriptor):
    audio = AudioSource(missing=colander.drop)


class DescriptorList(colander.SequenceSchema):
    descriptor = Descriptor()
    validator = colander.Length(min=1)


class QuestionElementOptions(colander.SchemaNode):
    fieldId = IdentifierString()
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
    id = IdentifierString()  # pylint: disable=invalid-name
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


class CalculateUnpromptedOptions(colander.SchemaNode):
    calculation = Expression()

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(CalculateUnpromptedOptions, self).__init__(*args, **kwargs)


UNPROMPTED_ACTION_OPTION_VALIDATORS = {
    'calculate': CalculateUnpromptedOptions(),
}


class Unprompted(colander.SchemaNode):
    action = UnpromptedAction()
    options = Options(missing=colander.drop)

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(Unprompted, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        action = cstruct.get('action', None)
        validator = UNPROMPTED_ACTION_OPTION_VALIDATORS.get(action, None)
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
                '"%s" actions do not accept options' % action,
            )


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

        for name, defn in iteritems(cstruct):
            sub_schema(IdentifierString, node, name)
            sub_schema(Unprompted, node, defn)


class ParameterType(colander.SchemaNode):
    schema_type = colander.String
    validator = colander.OneOf(PARAMETER_TYPES_ALL)


class ParameterOptions(colander.SchemaNode):
    type = ParameterType()

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(ParameterOptions, self).__init__(*args, **kwargs)


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
            sub_schema(IdentifierString, node, name)
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
        self._check_localizations(node, cstruct)

        if not self.instrument:
            return

        validate_instrument_version(
            self.instrument,
            cstruct,
            node.get('instrument'),
        )

        self._check_fields_covered(node, cstruct)

        self._check_type_specifics(node, cstruct)

    def _check_localizations(self, node, cstruct):
        checker = LocalizationChecker(node, cstruct['defaultLocalization'])

        def _ensure_element(element):
            if 'options' not in element:
                return
            options = element['options']

            checker.ensure(options, 'text', scope='Element Text')
            checker.ensure(options, 'help', scope='Element Help')
            checker.ensure(options, 'error', scope='Element Error')
            checker.ensure(options, 'audio', scope='Element Audio')
            checker.ensure(options, 'source', scope='Audio Source')

            for question in options.get('questions', []):
                _ensure_element(question)
            for enumeration in options.get('enumerations', []):
                checker.ensure_descriptor(enumeration, scope='Enumeration')
            for row in options.get('rows', []):
                checker.ensure_descriptor(row, scope='Matrix Row')

        checker.ensure(cstruct, 'title', node=node.get('title'))
        for page in cstruct['pages']:
            for element in page['elements']:
                _ensure_element(element)

    def _check_fields_covered(self, node, cstruct):
        instrument_fields = set([
            field['id']
            for field in self.instrument['record']
        ])

        form_fields = set()
        for page in cstruct['pages']:
            for element in page['elements']:
                if element['type'] != 'question':
                    continue

                field_id = element['options']['fieldId']
                if field_id in form_fields:
                    raise ValidationError(
                        node,
                        'Field "%s" is addressed by more than one question' % (
                            field_id,
                        )
                    )
                else:
                    form_fields.add(field_id)
        for field_id in iterkeys(cstruct.get('unprompted', {})):
            if field_id in form_fields:
                raise ValidationError(
                    node,
                    'Field "%s" is addressed by unprompted and a question' % (
                        field_id,
                    ),
                )
            else:
                form_fields.add(field_id)

        missing = instrument_fields - form_fields
        if missing:
            raise ValidationError(
                node,
                'There are Instrument fields which are missing: %s' % (
                    ', '.join(missing),
                )
            )

        extra = form_fields - instrument_fields
        if extra:
            raise ValidationError(
                node,
                'There are extra fields referenced by questions: %s' % (
                    ', '.join(extra),
                )
            )

    def _get_instrument_field(self, name):
        for field in self.instrument['record']:
            if field['id'] == name:
                return field

    def _check_type_specifics(self, node, cstruct):
        for page in cstruct['pages']:
            for element in page['elements']:
                if element['type'] != 'question':
                    continue

                type_def = get_full_type_definition(
                    self.instrument,
                    self._get_instrument_field(
                        element['options']['fieldId'],
                    )['type'],
                )

                if type_def['base'] not in ('enumeration', 'enumerationSet') \
                        and 'enumerations' in element['options']:
                    raise ValidationError(
                        node,
                        'Field "%s" cannot have an enumerations'
                        ' configuration' % (
                            element['options']['fieldId'],
                        ),
                    )

                self._check_matrix(node, type_def, element)
                self._check_subquestions(node, type_def, element)

    def _check_matrix(self, node, type_def, element):
        if type_def['base'] == 'matrix':
            instrument_rows = set([
                row['id']
                for row in type_def['rows']
            ])

            form_rows = set()
            for row in element['options'].get('rows', []):
                if row['id'] in form_rows:
                    raise ValidationError(
                        node,
                        'Row %s is addressed by more than one descriptor in'
                        ' %s' % (
                            row['id'],
                            element['options']['fieldId'],
                        ),
                    )
                else:
                    form_rows.add(row['id'])

            missing = instrument_rows - form_rows
            if missing:
                raise ValidationError(
                    node,
                    'There are missing rows in %s: %s' % (
                        element['options']['fieldId'],
                        ', '.join(missing),
                    )
                )

            extra = form_rows - instrument_rows
            if extra:
                raise ValidationError(
                    node,
                    'There are extra rows referenced by %s: %s' % (
                        element['options']['fieldId'],
                        ', '.join(extra),
                    )
                )

        elif 'rows' in element['options']:
            raise ValidationError(
                node,
                'Field "%s" cannot have a rows configuration' % (
                    element['options']['fieldId'],
                ),
            )

    def _check_subquestions(self, node, type_def, element):
        if type_def['base'] in ('matrix', 'recordList'):
            instrument_fields = set([
                field['id']
                for field in type_def[
                    'columns' if type_def['base'] == 'matrix' else 'record'
                ]
            ])

            form_fields = set()
            for subfield in element['options'].get('questions', []):
                if subfield['fieldId'] in form_fields:
                    raise ValidationError(
                        node,
                        'Subfield %s is addressed by more than one question in'
                        ' %s' % (
                            subfield['fieldId'],
                            element['options']['fieldId'],
                        ),
                    )
                else:
                    form_fields.add(subfield['fieldId'])

            missing = instrument_fields - form_fields
            if missing:
                raise ValidationError(
                    node,
                    'There are missing subfields in %s: %s' % (
                        element['options']['fieldId'],
                        ', '.join(missing),
                    )
                )

            extra = form_fields - instrument_fields
            if extra:
                raise ValidationError(
                    node,
                    'There are extra subfields referenced by %s: %s' % (
                        element['options']['fieldId'],
                        ', '.join(extra),
                    )
                )

        elif 'questions' in element['options']:
            raise ValidationError(
                node,
                'Field "%s" cannot have a questions configuration' % (
                    element['options']['fieldId'],
                ),
            )

