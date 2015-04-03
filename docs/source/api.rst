*************
API Reference
*************

.. contents:: Table of Contents

.. automodule:: prismh.core


Validation
==========

.. automodule:: prismh.core.validation
    :members:
    :exclude-members: ValidationError

.. py:exception:: ValidationError

    The exception thrown by the validation functions when the given input does
    not meet the PRISMH specifications.

    .. py:method:: asdict

        Returns a dictionary containing a summary of the problems found by the
        validator. The keys of the dictionary indiciate where in the structure
        the problem was found, and the values of the dictionary are a message
        explaining the issue.

        :rtype: dict


Output
======

.. automodule:: prismh.core.output
    :members:

