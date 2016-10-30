#!/usr/bin/env python3.4
# coding: utf-8

"""
This module defines a compiler class which can compile and dump a poop code
to a Python code object.
"""

import os
import sys
import ast
import marshal
import inspect
from functools import wraps

from poop.parser import Parser
from poop.prelude import default_env


class Compiler:
	"""
	Compiles an poop AST to a Python AST.
	"""

	translations = {}

	def __init__(self, ast, path=None):
		self.ast = ast
		self.path = path

	@classmethod
	def from_file(cls, path):
		"""
		Loads the poop AST from a given path.
		"""

		parser = Parser.from_file(path)
		ast = parser.run()
		return cls(ast, path)

	@classmethod
	def execute_compiled_file(cls, path, prelude=default_env, mute_env=False):
		"""
		Executes a Python code object stored in a file.
		"""

		if mute_env:
			env = prelude
		else:
			env = prelude.copy()

		with open(path, 'rb') as compiled_file:
			code = marshal.load(compiled_file)
			exec(code, env)

			_run_main_function(env)


	@classmethod
	def register(cls, *node_types):
		"""
		Registers a translation from an poop AST node to a Python AST node.
		"""

		def _decorator_wrapper(translation):
			@wraps(translation)
			def _translation_wrapper(self, node):
				py_node = translation(self, node)

				if node.pos is not None:
					py_node.lineno = node.pos.line

				return py_node

			for node_type in node_types:
				cls.translations[node_type] = _translation_wrapper

			return _translation_wrapper

		return _decorator_wrapper

	def translate(self, node):
		"""
		Translates an poop AST node into a Python AST node.
		"""

		py_ast = self.translations[type(node)](self, node)
		return ast.fix_missing_locations(py_ast)

	def compile(self):
		"""
		Compiles the poop AST to a Python code object.
		"""

		py_ast = self.translate(self.ast)

		code = compile(py_ast, self.path or '<string>', mode='exec')
		return code

	def dump(self, target=None):
		"""
		Dumps the Python code object to a given path.
		"""

		if target is None and self.path is None:
			raise ValueError('Unspecified target path')

		code = self.compile()
		target = target or os.path.basename(self.path).split('.')[0] + '.poopc'

		with open(target, 'wb') as dump_file:
			marshal.dump(code, dump_file)

	def load(self, env):
		"""
		Runs the code in the given environment.
		"""

		code = self.compile()

		exec(code, env)

	def execute(self, prelude=default_env, mute_env=False):
		"""
		Executes the resulting Python code object.
		"""

		if mute_env:
			env = prelude
		else:
			env = prelude.copy()

		self.load(env)
