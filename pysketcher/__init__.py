"""
Pysketcher is a simple tool which allows you to create
sketches of, e.g., mechanical systems in Python.
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
__version__ = '0.1'
__author__ = 'Hans Petter Langtangen <hpl@simula.no>'

from .shapes import *
