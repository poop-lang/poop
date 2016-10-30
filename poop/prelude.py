#!/usr/bin/env python3.4
# coding: utf-8

"""
This module defines the builtin values of poop.
"""

import random
import operator as op
from functools import reduce


default_env = {
	'shitspray': print,
    'random': random.randint,
    'eat': input,
    'tonumericpoop': int
}
