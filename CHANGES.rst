**************************
PRISMH.CORE Change History
**************************


0.3.0 (2015-06-17)
==================

* Added validation logic to Calculation Sets to make sure calculation IDs don't
  replicate Instrument Field IDs.
* Added validation logic to Calculation Sets that will check to see if Python
  expressions are valid syntax (only enabled on Python 2).
* Added validation logic to Calculation Sets that will check to see if HTSQL
  expressions are valid syntax (only enabled on Python 2 if HTSQL is
  installed).


0.2.1 (2015-06-10)
==================

* Widened the acceptible version range for the ``six`` dependency.


0.2.0 (2015-06-08)
==================

* Added a command line tool, ``prismh-validate``, to perform validations on
  files containing PRIMSH files.
* Expanded format of Web Form event targets to match updated specification.


0.1.1 (2015-05-29)
==================

* Fixed an issue where unprompted fields in Forms weren't being considered when
  verifying field coverage.


0.1.0 (2015-05-29)
==================

* Initial release for review.

