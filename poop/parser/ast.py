#!/usr/bin/env python3.4
# coding: utf-8

"""
Defines the AST structure of programs and expressions.
"""

__all__ = [
    'Node',                              # Base node
    'Program',                           # program AST
    'Stmt', 'Expr', 'Literal',           # abstract AST nodes
    'While', 'IfStmt',                   # control flow
    'Declaration', 'StmtExpr',           # statements
    'Call', 'BinOp', 'CmpOp',            # calls
    'Variable',                          # atom
    'IntLiteral', 'FloatLiteral',        # numeric literal
    'CharLiteral', 'StringLiteral'       # string-related literals
]


class Node:
    """
    Abstract Acid AST node.
    """

    def __init__(self):
        self.span = None

    @property
    def pos(self):
        if self.span is not None:
            return self.span.start

    @classmethod
    def sub_types(cls):
        for sub_type in cls.__subclasses__():
            yield sub_type
            yield from sub_type.sub_types()


class Program(Node):
    """
    Represents a sequence of instructions.
    """

    def __init__(self, instructions, path=None):
        super().__init__()
        self.path = path
        self.instructions = instructions

    def __repr__(self):
        fmt = 'Program(path={0.path!r}, instructions={0.instructions})'
        return fmt.format(self)


class Stmt(Node):
    """
    Abstract AST element representing a top-level statement.
    """


class StmtExpr(Stmt):
    """
    An expression statement.
    """

    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return 'StmtExpr(expr={0.expr!r})'.format(self)


class While(Stmt):
    """
    Looping while a condition is verified.
    """

    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def __repr__(self):
        return 'While(cond={0.cond!r}, body={0.body!r})'.format(self)


class Declaration(Stmt):
    """
    Declaring a name.
    """

    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value

    def __repr__(self):
        return 'Declaration(name={0.name!r}, value={0.value!r})'.format(self)


class IfStmt(Stmt):
    """
    Conditional control structure.
    """

    def __init__(self, cond, body, else_body=()):
        super().__init__()
        self.cond = cond
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        return 'IfStmt(cond={0.cond!r}, body={0.body!r}, else_body={0.else_body!r})'.format(self)


class Expr(Node):
    """
    Abstract AST element representing an expression node.
    """


class Call(Expr):
    """
    Function call.
    """

    def __init__(self, func, args):
        super().__init__()
        self.func = func
        self.args = args

    def __repr__(self):
        return 'Call(func={0.func!r}, args={0.args})'.format(self)


class BinOp(Expr):
    """
    Binary infix operation.
    """

    def __init__(self, lhs, op, rhs):
        self.lhs, self.rhs =lhs, rhs
        self.op = op

    def __repr__(self):
        return 'BinOp(lhs={0.lhs!r}, op={0.op!r}, rhs={0.rhs!r})'.format(self)


class CmpOp(Expr):
    """
    Binary infix comparison.
    """

    def __init__(self, lhs, op, rhs):
        self.lhs, self.rhs =lhs, rhs
        self.op = op

    def __repr__(self):
        return 'CmpOp(lhs={0.lhs!r}, op={0.op!r}, rhs={0.rhs!r})'.format(self)


class Variable(Expr):
    """
    Variable name.
    """

    def __init__(self, name):
        super().__init__()
        self.name = name

    def __repr__(self):
        return 'Variable(name={0.name!r})'.format(self)


class Literal(Expr):
    """
    Abstract literal expression.
    """

    def __init__(self, value):
        super().__init__()
        self.value = value

    def __repr__(self):
        return '{0.__class__.__name__}(value={0.value!r})'.format(self)


class IntLiteral(Literal):
    """
    Integer literal expression.
    """


class FloatLiteral(Literal):
    """
    Floating point number literal expression.
    """


class CharLiteral(Literal):
    """
    Literal character. May be escaped.
    """


class StringLiteral(Literal):
    """
    Literal sequence of potentially escaped characters.
    """
