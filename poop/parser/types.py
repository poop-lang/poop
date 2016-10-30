#!/usr/bin/env python3.4
# coding: utf-8

"""
Defines some types that are used by several modules in the package.
"""


class SourcePos:
	"""
	Represents a position in a file.
	"""

	def __init__(self, line, column):
		self.line, self.column = line, column

	def __repr__(self):
		return 'SourcePos(line={pos.line}, col={pos.column})'.format(pos=self)

	def __str__(self):
		return 'line {pos.line}, column {pos.column}'.format(pos=self)

	def feed(self, string):
		"""
		Updates the position from a given string.

		Note: This code assumes that the string contains UNIX line terminators.
		"""

		for char in string:
			if char == '\n':
				self.line += 1   # increment line
				self.column = 1  # reset column index
			else:
				self.column += 1

	def copy(self):
		"""
		Copies the instance to avoid unwanted references.
		"""

		return SourcePos(line=self.line, column=self.column)


class SourceSpan:
	"""
	Represents a span between two positions in a file.
	"""

	def __init__(self, start, end):
		self.start = start
		self.end = end

	def __repr__(self):
		return 'SourceSpan(start={0.start!r}, end={0.end!r})'.format(self)

	def __str__(self):
		if self.start.line == self.end.line:
			fmt = 'line {line} from column {start} to column {end}'
			return fmt.format(line=self.start.line,
					   		  start=self.start.column,
					   		  end=self.end.column)

		else:
			return '{0.start!s} to {0.end!s}'.format(self)

	@classmethod
	def between(cls, first, last):
		return cls(first.span.start, last.span.end)
