#!/usr/bin/env python3.4
# coding: utf-8

"""
Defines an AST to represent a REPL command.
"""

import os

from poop.parser import *
from poop.compiler import Compiler


class REPLCommand:
    """
    Base class of all REPL commands.
    """

    def execute(self, repl):
        """
        Executed when the users types the command.
        """

        msg = '`execute` is not defined for type {!r}.'.format(self.__class__)
        raise NotImplementedError(msg)


class Newline(REPLCommand):
    """
    Skips an empty or whitespace line.
    """

    def execute(self, repl):
        pass


class EvalStmt(REPLCommand):
    """
    Evals a poop statement in the REPL environment.
    """

    def __init__(self, stmt):
        self.stmt = stmt

    def execute(self, repl):
        module = Program(instructions=[self.stmt])
        compiler = Compiler(module)
        compiler.load(repl.environment)


class EvalExpr(REPLCommand):
    """
    Evals a poop expression in the REPL environment.
    """

    def __init__(self, expr):
        self.expr = expr

    def execute(self, repl):
        stmt = Declaration(name='_', value=self.expr)
        module = Program(instructions=[stmt])
        compiler = Compiler(module)

        compiler.load(repl.environment)

        return repl.environment.get('_', None)


class Command(REPLCommand):
    """
    Executes a REPL command with given arguments.
    """

    def __init__(self, name, args):
        self.name = name
        self.args = args

    def execute(self, repl):
        try:
            args = []
            for arg in self.args:
                args.append(EvalExpr(arg).execute(repl))

            return repl.get_command(self.name)(repl, *args)
        except KeyError:
            print('Unknown command {!r}, please type :help to see the list of '
                  'commands'.format(self.name))


class OSCommand(REPLCommand):
    """
    Executes an OS command.
    """

    def __init__(self, cmd):
        self.cmd = cmd

    def execute(self, repl):
        os.system(self.cmd)
