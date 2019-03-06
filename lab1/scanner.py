import ply.lex as lex

reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'for' : 'FOR',
    'while' : 'WHILE',
    'break' : 'BREAK',
    'continue' : 'CONTINUE',
    'return' : 'return',
    'eye' : 'EYE',
    'zeros' : 'ZEROS',
    'ones' : 'ONES',
    'print' : 'PRINT'
}

tokens = (
          'COMMENT',

          'DOTADD',
          'DOTSUB',
          'DOTMUL',
          'DOTDIV',

          'ADDASSIGN',
          'SUBASSIGN',
          'MULASSIGN',
          'DIVASSIGN',

          'ADD',
          'SUB',
          'MUL',
          'DIV',

          'LESS_EQUAL',
          'GREATER_EQUAL',
          'NOT_EQUAL',
          'EQUAL',
          'ASSIGN',
          'LESS',
          'GREATER',

          'LPAREN',
          'RPAREN',
          'LPAREN_SQUARE',
          'RPAREN_SQUARE',
          'LPAREN_CURLY',
          'RPAREN_CURLY',

          'FLOATNUM',
          'INTNUM',

          'SLICE',
          'TRANSPOSE',
          'COMMA',
          'COLON',

          'STRING',
          'ID') + tuple(reserved.values())


def t_COMMENT(t):
    r'\#.*'
    pass
    # return t

t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'

t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='

t_ADD    = r'\+'
t_SUB   = r'-'
t_MUL   = r'\*'
t_DIV  = r'/'

t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_NOT_EQUAL = '!='
t_EQUAL = '=='
t_ASSIGN = '='
t_LESS = '<'
t_GREATER = '>'

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LPAREN_SQUARE = r'\['
t_RPAREN_SQUARE = r']'
t_LPAREN_CURLY = r'{'
t_RPAREN_CURLY = r'}'

t_SLICE = r':'
t_TRANSPOSE = r'\''
t_COMMA = r','
t_COLON = r';'

t_STRING = r'"[^"]*"'


def t_FLOATNUM(t):
    r'([0-9]+\.[0-9]*|[0-9]*\.[0-9]+)([Ee][+-]?[0-9]*)?'
    t.value = float(t.value)
    return t

def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value, 'ID')
    return t


literals = "+-*/()"

t_ignore = '  \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t) :
    print("Illegal character '%s'" %t.value[0])
    t.lexer.skip(1)


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


lexer = lex.lex()

