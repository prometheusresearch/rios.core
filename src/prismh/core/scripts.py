#
# Copyright (c) 2015, Prometheus Research, LLC
#


import argparse
import codecs
import pkg_resources
import sys

from six import iteritems

from .validation import *


__all__ = (
    'ValidationScript',
    'validate',
)


VALIDATORS = {
    'instrument': lambda x, instrument: validate_instrument(x),
    'assessment': validate_assessment,
    'calculationset': validate_calculationset,
    'form': validate_form,
    'interaction': validate_interaction,
}


class ValidationScript(object):
    def __init__(self):
        self._stdout = None

        self.parser = argparse.ArgumentParser(
            description='A tool for validating the format of PRISMH files.',
        )

        try:
            self_version = \
                pkg_resources.get_distribution('prismh.core').version
        except pkg_resources.DistributionNotFound:  # pragma: no cover
            self_version = 'UNKNOWN'
        self.parser.add_argument(
            '-v',
            '--version',
            action='version',
            version='%(prog)s ' + self_version,
        )

        self.parser.add_argument(
            'spectype',
            choices=[
                'instrument',
                'assessment',
                'calculationset',
                'form',
                'interaction',
            ],
            help='The type of PRISMH file to validate.',
        )

        self.parser.add_argument(
            'filename',
            type=argparse.FileType('r', 0),
            help='The file containing the structure to validate. To read from'
            ' standard input, specify a "-" here.',
        )

        self.parser.add_argument(
            '-i',
            '--instrument',
            type=argparse.FileType('r', 0),
            help='The file containing the Common Instrument Definition to'
            ' validate against. To read from standard input, specify a "-"'
            ' here.',
        )

    def __call__(self, argv=None, stdout=sys.stdout):
        args = self.parser.parse_args(argv)
        self._stdout = stdout

        input_file = codecs.EncodedFile(args.filename, 'utf-8')
        input_file_name = input_file.stream.name

        instrument_file = None
        if args.instrument:
            instrument_file = codecs.EncodedFile(args.instrument, 'utf-8')

        try:
            VALIDATORS[args.spectype](input_file, instrument=instrument_file)
        except ValidationError as exc:
            self.out('%s failed validation.' % input_file_name)
            for source, message in iteritems(exc.asdict()):
                self.out('%s: %s' % (
                    source,
                    message,
                ))
            return 1
        else:
            self.out('%s successfully validated.' % input_file_name)
            return 0

    def out(self, message):
        self._stdout.write('%s\n' % (message,))


validate = ValidationScript()  # pylint: disable=invalid-name

