#!/usr/bin/env python3.4
# coding: utf-8

"""
Defines some types and functions for tokenizing a given code string.
"""

__all__ = ['TokenType', 'Token', 'tokenize', 'BIN_OP', 'CMP_OP']


import re
import ast
from enum import Enum
from itertools import dropwhile

from poop.parser.types import SourcePos, SourceSpan
from poop.exception import ParseError

BIN_OP = {
    '+': ast.Add,
    '-': ast.Sub,
    '*': ast.Mult,
    '/': ast.Div,
    '^': ast.Pow
}

CMP_OP = {
    '==': ast.Eq,
    '!=': ast.NotEq,
    '<': ast.Lt,
    '>': ast.Gt,
    '<=': ast.LtE,
    '>=': ast.GtE,
}


# derive from Enum to allow iteration through the token types
class TokenType(Enum):
    """
    Lists every token type and stores their regular expression pattern.
    """

    def __init__(self, pattern):
        self.regex = re.compile(pattern)

    UNZIP_PANTS = r'unzip pants'
    FLUSH_TOILETS = r'flush toilets'
    CONSTIPATED_WHILE = r'constipated while'
    WIPE = r'wipe'
    STINKY = r'stinky'
    IS = r'is'
    READ = r'read'
    IF = r'if'
    ELSEIF = r'elseif'
    ELSE = r'else'
    SPLOSH = r'splosh'

    COMMA = r','

    BIN_OP = '(' + '|'.join(map(re.escape, BIN_OP)) + ')'
    CMP_OP = '(' + '|'.join(map(re.escape, CMP_OP)) + ')'

    LINE_COMMENT = r'//'
    COMMENT_START, COMMENT_END = r'/\*', r'\*/'

    LPAREN, RPAREN = r'\(', r'\)'

    CHAR_LITERAL = r"'([^'\\]|\\.)'"
    STRING_LITERAL = r'"([^"\\]|\\.)*"'
    FLOAT_LITERAL = r'\d+\.\d+ tons? of shit'
    INT_LITERAL = r'(\d+) tons? of shit'

    IDENT = r'\w+'

    NEWLINE = r'[\n\r]+'
    WHITESPACE = r'\s+'


class Token:
    """
    Concrete lexeme type.
    """

    def __init__(self, type, value, span):
        self.type = type
        self.value = value
        self.span = span

    def __repr__(self):
        fmt = 'Token(type={tok.type}, value={tok.value!r}, span={tok.span!r})'
        return fmt.format(tok=self)

    @property
    def pos(self):
        return self.span.start


def tokenize(code):
    """
    Chop the given string in Token instances.
    """

    cursor = SourcePos(line=1, column=1)

    while code:
        # iterates over all TokenType instances in order
        for token_type in TokenType:
            match = token_type.regex.match(code)

            if match is not None:
                # source position before the code is consumed
                startpos = cursor.copy()

                # pop the matched string
                code = code[match.end():]

                # value is assigned to the entire match string
                value = match.group(0)

                # update cursor position (line and column index)
                cursor.feed(value)

                if token_type == TokenType.LINE_COMMENT:
                    # drop every character until newline
                    code = ''.join(dropwhile(lambda c: c != '\n', code))

                elif token_type == TokenType.COMMENT_START:
                    # test if the code matches a comment ending token
                    m = TokenType.COMMENT_END.regex.match(code)

                    # while the comment block is not ended
                    while m is None:
                        # feed a character from the comment string
                        cursor.feed(code[0])

                        # pop a single character
                        code = code[1:]

                        # retest if the code matches a comment ending token
                        m = TokenType.COMMENT_END.regex.match(code)

                    # pop the matched string
                    code = code[m.end():]

                # skipping whitespace
                elif token_type is not TokenType.WHITESPACE:
                        # copy the cursor to avoid unwanted reference
                        endpos = cursor.copy()

                        span = SourceSpan(startpos, endpos)
                        tok = Token(token_type, value, span)
                        yield tok

                break
        else:
            # when every token type has been tried
            raise ParseError(code, cursor, "Failed to tokenize code")
