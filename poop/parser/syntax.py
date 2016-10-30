#!/usr/bin/env python3.4
# coding: utf-8

"""
This module defines the parser rules. To define a custom parser rule, use this
snippet as a template:

    @Parser.register([NodeType], priority=[n])
    def [rule_name](self):
        # To consume a token of a given type:
        expected_token = self.expect([token type])

        node = self.consume([NodeType to consume])

        ...  # Processing tokens

        return [AST node]
"""

from poop.parser.parser import Parser
from poop.parser.lexer import *
from poop.parser.ast import *
from poop.parser.types import SourceSpan
from poop.exception import *


@Parser.register(Program, priority=1)
def consume_program(self):
    # the program instructions
    instrs = []

    self.expect(TokenType.UNZIP_PANTS)
    self.expect(TokenType.NEWLINE)

    while self.token_queue:
        try:
            # tries to parse an expression from the token queue
            instr = self.consume(Stmt)
        except ParseError:
            raise  # when no expression could be parsed
        else:
            # append the instruction to the program
            instrs.append(instr)

    # returns the resulting Program object.
    prog = Program(instrs, self.path)
    prog.span = SourceSpan.between(instrs[0], instrs[-1])
    return prog


@Parser.register(Declaration, priority=1)
def consume_declaration(self):
    first = self.expect(TokenType.STINKY)
    ident = self.expect(TokenType.IDENT)
    name = ident.value

    self.expect(TokenType.IS)

    value = self.consume(Expr)

    last = self.expect(TokenType.NEWLINE)

    decl = Declaration(name, value)
    decl.span = SourceSpan.between(first, last)
    return decl


@Parser.register(Call, priority=1)
def consume_call(self):
    func = self.expect(TokenType.IDENT)
    self.expect(TokenType.LPAREN)

    args = []

    try:
        first = self.consume(Expr)
    except ParseError:
        pass
    else:
        args.append(first)

    while self.token_queue[0].type == TokenType.COMMA:
        self.token_queue.pop(0)

        try:
            nxt = self.consume(Expr)
        except ParseError:
            break
        else:
            args.append(nxt)

    last = self.expect(TokenType.RPAREN)

    call = Call(func.value, args)
    call.span = SourceSpan.between(func, last)
    return call


@Parser.register(BinOp, priority=2)
def consume_binop(self):
    first = self.expect(TokenType.LPAREN)
    lhs = self.consume(Expr)
    op = self.expect(TokenType.BIN_OP)
    rhs = self.consume(Expr)
    last = self.expect(TokenType.RPAREN)

    binop = BinOp(lhs, op.value, rhs)
    binop.span = SourceSpan.between(first, last)
    return binop


@Parser.register(CmpOp, priority=2)
def consume_binop(self):
    first = self.expect(TokenType.LPAREN)
    lhs = self.consume(Expr)
    op = self.expect(TokenType.CMP_OP)
    rhs = self.consume(Expr)
    last = self.expect(TokenType.RPAREN)

    cmpop = CmpOp(lhs, op.value, rhs)
    cmpop.span = SourceSpan.between(first, last)
    return cmpop


@Parser.register(StmtExpr, priority=1)
def consume_stmt_expr(self):
    expr = self.consume(Expr)
    self.expect(TokenType.NEWLINE)
    stmt = StmtExpr(expr)
    stmt.span = expr.span
    return stmt


@Parser.register(While, priority=2)
def consume_while(self):
    first = self.expect(TokenType.CONSTIPATED_WHILE)
    cond = self.consume(Expr)
    self.expect(TokenType.NEWLINE)
    body = []

    while True:
        try:
            nxt = self.consume(Stmt)
        except ParseError:
            break
        else:
            body.append(nxt)

    self.expect(TokenType.SPLOSH)
    last = self.expect(TokenType.NEWLINE)

    while_ = While(cond, body)
    while_.span = SourceSpan.between(first, last)
    return while_


@Parser.register(IfStmt, priority=2)
def consume_while(self):
    first = self.expect(TokenType.IF)
    cond = self.consume(Expr)
    self.expect(TokenType.NEWLINE)

    body = []
    else_body = []

    while True:
        try:
            nxt = self.consume(Stmt)
        except ParseError:
            break
        else:
            body.append(nxt)

    if self.token_queue[0].type == TokenType.SPLOSH:
        self.token_queue.pop(0)
    elif self.token_queue[0].type == TokenType.ELSE:
        self.token_queue.pop(0)
        self.expect(TokenType.NEWLINE)

        while True:
            try:
                nxt = self.consume(Stmt)
            except ParseError:
                break
            else:
                else_body.append(nxt)

        self.expect(TokenType.SPLOSH)

    last = self.expect(TokenType.NEWLINE)

    if_ = IfStmt(cond, body, else_body)
    if_.span = SourceSpan.between(first, last)
    return if_


@Parser.register(Variable, priority=2)
def consume_variable(self):
    ident = self.expect(TokenType.IDENT)

    var = Variable(ident.value)
    var.span = ident.span
    return var


@Parser.register(IntLiteral, priority=1)
def consume_int_literal(self):
    token = self.expect(TokenType.INT_LITERAL)

    str_val = token.value.split()[0]
    lit = IntLiteral(int(str_val))
    lit.span = token.span
    return lit


@Parser.register(FloatLiteral, priority=1)
def consume_float_literal(self):
    token = self.expect(TokenType.FLOAT_LITERAL)

    str_val = token.value.split()[0]
    lit = FloatLiteral(float(str_val))
    lit.span = token.span
    return lit


@Parser.register(CharLiteral, priority=1)
def consume_char_literal(self):
    token = self.expect(TokenType.CHAR_LITERAL)
    char = token.value.strip("'")

    lit = CharLiteral(char)
    lit.span = token.span
    return lit


@Parser.register(StringLiteral, priority=1)
def consume_string_literal(self):
    token = self.expect(TokenType.STRING_LITERAL)

    # todo: find another way to unescape strings
    string = token.value.strip('"').encode('latin-1').decode('unicode_escape')

    lit = StringLiteral(string)
    lit.span = token.span
    return lit
