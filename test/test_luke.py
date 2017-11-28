#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Test script for luke
Latest version can be found at https://github.com/letuananh/chirptext

References:
    Python unittest documentation:
        https://docs.python.org/3/library/unittest.html
    Python documentation:
        https://docs.python.org/
    PEP 0008 - Style Guide for Python Code
        https://www.python.org/dev/peps/pep-0008/
    PEP 0257 - Python Docstring Conventions:
        https://www.python.org/dev/peps/pep-0257/

@author: Le Tuan Anh <tuananh.ke@gmail.com>
'''

# Copyright (c) 2017, Le Tuan Anh <tuananh.ke@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__author__ = "Le Tuan Anh"
__email__ = "<tuananh.ke@gmail.com>"
__copyright__ = "Copyright 2017, chirptext"
__license__ = "MIT"
__maintainer__ = "Le Tuan Anh"
__version__ = "0.1"
__status__ = "Prototype"
__credits__ = []

########################################################################

import os
import unittest
from chirptext.luke import Word, read_swadesh_1971, read_swadesh_ranked, read_swadesh_sign

# -------------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------------

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DATA = os.path.join(TEST_DIR, 'data')


# -------------------------------------------------------------------------------
# Test cases
# -------------------------------------------------------------------------------

class TestLuke(unittest.TestCase):

    def test_swadesh(self):
        s71 = read_swadesh_1971()
        sr = read_swadesh_ranked()
        ss = read_swadesh_sign()
        self.assertEqual(len(s71), 100)
        self.assertEqual(len(sr), 100)
        self.assertEqual(len(ss), 100)
        # are they the same words?
        s71_words = {w.word for w in s71}
        sr_words = {w.word for w in sr}
        self.assertEqual(s71_words, sr_words)
        ss_words = {w.word for w in ss}
        self.assertEqual(len(ss_words), 100)
        # validate words
        same = ss_words.intersection(s71_words)
        diff = ss_words.difference(s71_words)
        self.assertEqual(same, {'die', 'red', 'stone', 'lie', 'leaf', 'grease', 'not', 'tree', 'mountain', 'black', 'kill', 'night', 'egg', 'louse', 'who', 'blood', 'green', 'what', 'rain', 'dry', 'good', 'sit', 'white', 'new', 'man', 'all', 'full', 'fire', 'bird', 'tail', 'woman', 'moon', 'yellow', 'water', 'name', 'feather', 'long', 'sun', 'star', 'stand', 'fish', 'dog', 'person', 'earth'})
        self.assertEqual(diff, {'when', 'wide', 'smooth', 'snow', 'laugh', 'with', 'warm', 'child', 'brother', 'cat', 'sing', 'how', 'correct', 'worm', 'dust', 'sharp', 'pig', 'play', 'meat', 'grass', 'ice', 'dull', 'short', 'animal', 'if', 'river', 'day', 'sea', 'heavy', 'other', 'wife', 'year', 'rope', 'wind', 'narrow', 'because', 'wet', 'salt', 'dirty', 'vomit', 'live', 'father', 'snake', 'husband', 'work', 'old', 'sister', 'mother', 'count', 'flower', 'dance', 'where', 'hunt', 'thin', 'wood', 'bad'})


# -------------------------------------------------------------------------------
# Main method
# -------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
