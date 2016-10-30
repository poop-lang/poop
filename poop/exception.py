#!/usr/bin/env python3.4
# coding: utf-8

"""
This module defines some exception that may be raised during tokenizing,
parsing, or execution.
"""


class ParseError(ValueError):
	"""
	Raised when the parser fails to parse the code.
	"""

	def __init__(self, code, pos, msg):
		self.code = code
		self.pos = pos
		self.msg = msg

	@property
	def line(self):
		lines = self.code.splitlines()
		return lines[self.pos.line - 1]

	def __str__(self):
		return """
`{err.line}`
{cursor_margin}^
Parser failed to parse the code at {err.pos}:
{err.msg}
""".format(err=self, cursor_margin=' ' * self.pos.column)
