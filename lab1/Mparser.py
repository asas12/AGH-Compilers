#!/usr/bin/python

import scanner
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    ('nonassoc', 'RETURN'),
    ('nonassoc', 'IF_NELSE'),
    ('nonassoc', 'ELSE'),
    ('nonassoc', 'ID'),
    ('left', '[', ']'),
    ('left', '=', 'ADDASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'MULASSIGN'),
    ('left', '<', '>', 'LESS_EQUAL','GREATER_EQUAL', 'NOT_EQUAL', 'EQUAL'),
    ('left', '+', '-', 'DOTADD', 'DOTSUB'),
    ('left', '*', '/', 'DOTMUL', 'DOTDIV'),
    ('right', 'UMINUS'),
    ('left', 'TRANSPOSE')
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')"
              .format(p.lineno, scanner.find_column(parser.text, p), p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""


def p_instructions_opt_1(p):
    """instructions_opt : instructions """


def p_instructions_opt_2(p):
    """instructions_opt : """


def p_instructions_1(p):
    """instructions : instructions instruction """


def p_instructions_2(p):
    """instructions : instruction """


def p_instruction_expression(p):
    """instruction : expression ';' """


def p_instruction_if(p):
    """instruction : IF '(' condition ')' instruction %prec IF_NELSE"""


def p_instruction_if_else(p):
    """instruction : IF '(' condition ')' instruction ELSE instruction"""


def p_instruction_for(p):
    """instruction : FOR ID '=' expression ':' expression instruction"""


def p_instruction_while(p):
    """instruction : WHILE '(' condition ')' instruction"""


def p_instruction_complex(p):
    """instruction : '{' instructions '}' """


def p_condition(p):
    """condition : expression LESS_EQUAL expression
                 | expression GREATER_EQUAL expression
                 | expression NOT_EQUAL expression
                 | expression EQUAL expression
                 | expression '<' expression
                 | expression '>' expression"""


def p_expression_floatnum(p):
    """ expression : FLOATNUM"""


def p_expression_intnum(p):
    """ expression : INTNUM """


def p_expression_id(p):
    """ expression : ID """


def p_expression_array_index(p):
    """expression : ID '[' numbers ']' """


def p_matrix_expression(p):
    """ expression : matrix"""


def p_matrix(p):
    """matrix : '['  matrices ']'
                  | '[' vectors ']' """


def p_matrices(p):
    """ matrices :  matrix  ',' matrices
                 | matrix """


def p_vectors(p):
    """ vectors : vectors ';' numbers
                | numbers"""


def p_numbers(p):
    """ numbers : numbers ',' number
                | number """


def p_number(p):
    """ number : ID
               | FLOATNUM
               | INTNUM"""


def p_expression_binary_operators(p):
    """ expression : expression '+' expression
                   | expression '-' expression
                   | expression '/' expression
                   | expression '*' expression"""
   # if p[2] == '+':
   #     p[0] = p[1] + p[3]
   # else:
   #     if p[2] == '-':
   #         p[0] = p[1] - p[3]
   #     else:
   #         if p[2] == '/':
   #             p[0] = p[1] / p[3]
   #         else:
   #             if p[2] == '*':
   #                 p[0] = p[1] * p[3]


def p_dot_operators(p):
    """expression : expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression"""


def p_assign(p):
    """expression : expression '=' expression
                  | expression ADDASSIGN expression
                  | expression SUBASSIGN expression
                  | expression MULASSIGN expression
                  | expression DIVASSIGN expression"""


def p_transpose(p):
    """ expression : expression TRANSPOSE """


def p_negation(p):
    """expression : '-' expression %prec UMINUS"""
    #p[0] = -p[1]


def p_string(p):
    """expression : STRING """


def p_functions(p):
    """ expression : ZEROS '(' expression ')'
                   | ONES '(' expression ')'
                   | EYE '(' expression ')'
                   | PRINT '(' expression ')'
                   | PRINT STRING
                   | PRINT numbers"""


def p_key_phrases(p):
    """ expression : BREAK
                   | CONTINUE
                   | COMMENT
                   | RETURN expression"""


parser = yacc.yacc()
