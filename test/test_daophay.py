#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Test Dao Phay library
Latest version can be found at https://github.com/letuananh/pydemo

References:
	Python documentation:
		https://docs.python.org/
	Python unittest
		https://docs.python.org/3/library/unittest.html
	PEP 257 - Python Docstring Conventions:
		https://www.python.org/dev/peps/pep-0257/

@author: Le Tuan Anh <tuananh.ke@gmail.com>
'''

# Copyright (c) 2015, Le Tuan Anh <tuananh.ke@gmail.com>
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

__author__ = "Le Tuan Anh <tuananh.ke@gmail.com>"
__copyright__ = "Copyright 2015, chirptext"
__credits__ = [ "Le Tuan Anh" ]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Le Tuan Anh"
__email__ = "<tuananh.ke@gmail.com>"
__status__ = "Prototype"

########################################################################

import sys
import os
import argparse
import unittest
from daophay import DaoPhay

########################################################################

class TestDaoPhay(unittest.TestCase):

	def vn_sorted_arrays(self, inputs, expected):
		#inputs = []
		#expected = []
		actual = DaoPhay.vn_sorted(inputs)
		self.assertEqual(expected, actual)

	def test_vn_sorted(self):
		print("Test vn sorting")
		self.vn_sorted_arrays([], [])
		self.vn_sorted_arrays(['anh', 'an'], ['an', 'anh'])
		self.vn_sorted_arrays(['uống', 'uốn', 'ương' ], ['uốn', 'uống', 'ương' ])

	


########################################################################

def main():
	unittest.main()

if __name__ == "__main__":
	main()