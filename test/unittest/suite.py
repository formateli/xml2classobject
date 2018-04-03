# This file is part of Xml2ClassObject project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

"Xml2ClassObject unittest suite"

import os
import sys
import unittest

DIR = os.path.dirname(os.path.realpath(__file__))
DIR = os.path.normpath(os.path.join(DIR, '..', '..', 'xml2classobject'))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))

import xml2classobjecttest


LOADER = unittest.TestLoader()

SUITE = LOADER.loadTestsFromModule(xml2classobjecttest)

RUNNER = unittest.TextTestRunner(verbosity=2)
RESULT = RUNNER.run(SUITE)
