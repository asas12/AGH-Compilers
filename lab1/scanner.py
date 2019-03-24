import ply.lex as lex

import ply.yacc as yacc


reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT'
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


          'LESS_EQUAL',
          'GREATER_EQUAL',
          'NOT_EQUAL',
          'EQUAL',

          'FLOATNUM',
          'INTNUM',

          'TRANSPOSE',

          'STRING',
          'ID') + tuple(reserved.values())

literals = r"+-*/(){}[]:<>=,;"


def t_COMMENT(t):
    r'\#.*'
    pass
    # return t


t_TRANSPOSE = r'\''
t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'

t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='


t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_NOT_EQUAL = '!='
t_EQUAL = '=='


#t_STRING = r'"[^"]*"'
#t_STRING = r'"([^"]?(\\")?)*"'
def t_STRING(t):
    r'"([^\\"]+|\\.)*"'
    t.value = t.value[1:-1]
    #t.value = re.sub()
    return t


def t_FLOATNUM(t):
    r'([0-9]+\.[0-9]*|\.[0-9]+)([Ee][+-]?[0-9]*)?'
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



#literals = ['+','-']#,'*','/','(',')','{','}','[',']','.',':','<','>','=',',',';','\'']


t_ignore = '  \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t) :
    print("Illegal character '%s'" %t.value[0])
    t.lexer.skip(1)


def find_column(text, token):
    line_start = text.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1



lexer = lex.lex()



