#!/usr/bin/env python3.4
# coding: utf-8

"""
This module defines some conversions between poop's and Python's AST nodes.
"""

import ast as python_ast

from poop.compiler.compiler import Compiler
from poop.parser.lexer import BIN_OP, CMP_OP
from poop.parser.ast import *


@Compiler.register(Program)
def translate_program(compiler, program):
	instrs = map(compiler.translate, program.instructions)
	module = python_ast.Module(body=list(instrs))
	return module


@Compiler.register(While)
def translate_while(compiler, while_):
    instrs = list(map(compiler.translate, while_.body))
    return python_ast.While(
        test=compiler.translate(while_.cond),
        body=instrs,
        orelse=[]
    )


@Compiler.register(IfStmt)
def translate_while(compiler, if_):
    instrs = list(map(compiler.translate, if_.body))
    else_instrs = list(map(compiler.translate, if_.else_body))
    return python_ast.If(
        test=compiler.translate(if_.cond),
        body=instrs,
        orelse=else_instrs
    )


@Compiler.register(StmtExpr)
def translate_stmt_expr(compiler, stmt):
    return python_ast.Expr(
        value=compiler.translate(stmt.expr)
    )


@Compiler.register(Declaration)
def translate_declaration(compiler, declaration):
	assign = python_ast.Assign()
	assign.targets = [
		python_ast.Name(id=declaration.name, ctx=python_ast.Store())
	]
	assign.value = compiler.translate(declaration.value)
	return assign


@Compiler.register(Call)
def translate_call(compiler, call):
	return python_ast.Call(
		func=python_ast.Name(call.func, python_ast.Load()),
		args=list(map(compiler.translate, call.args)),
		keywords=[]
	)


@Compiler.register(BinOp)
def translate_binop(compiler, binop):
    return python_ast.BinOp(
        left=compiler.translate(binop.lhs),
        op=BIN_OP[binop.op](),
        right=compiler.translate(binop.rhs)
    )

@Compiler.register(CmpOp)
def translate_cmpop(compiler, cmpop):
    return python_ast.Compare(
        left=compiler.translate(cmpop.lhs),
        ops=[CMP_OP[cmpop.op]()],
        comparators=[compiler.translate(cmpop.rhs)]
    )

@Compiler.register(Variable)
def translate_variable(compiler, var):
	return python_ast.Name(var.name, python_ast.Load())


@Compiler.register(IntLiteral, FloatLiteral)
def translate_num(compiler, num):
	return python_ast.Num(num.value)


@Compiler.register(CharLiteral, StringLiteral)
def translate_string_or_char(compiler, string_or_char):
	return python_ast.Str(string_or_char.value)
