#!/usr/bin/python

import scanner
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    ('nonassoc', 'RETURN'),
    ('nonassoc', 'IF_NELSE'),
    ('nonassoc', 'ELSE'),
    ('nonassoc', 'ID'),
    ('nonassoc', 'PRINT'),
    ('left', '[', ']'),
    ('right', '=', 'ADDASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'MULASSIGN'),
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
    """instruction : FOR id '=' expression ':' expression instruction"""


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


def p_numeric_expression(p):
    """expression : int
                  | float"""


def p_expression_floatnum(p):
    """ float : FLOATNUM"""


def p_expression_intnum(p):
    """ int : INTNUM """


def p_expression_lvalue(p):
    """ expression : lvalue
        lvalue : id
               | id_arr"""


def p_expression_id(p):
    """ id : ID """


def p_expression_array_index(p):
    """id_arr : ID '[' int_numbers ']' """


# contains int numbers and ids - used for indexing
def p_int_numbers(p):
    """ int_numbers : int_numbers ',' int_number
                | int_number"""


def p_number(p):
    """int_number : id
              | int"""


def p_matrix_expression(p):
    """ expression : matrix"""


def p_matrix(p):
    """matrix : '['  matrices ']'
                  | '[' vectors ']' """


def p_matrices(p):
    """ matrices :  matrix  ',' matrices
                 | matrix """


def p_vectors(p):
    """ vectors : vectors ';' numerics
                | numerics"""


def p_numerics(p):
    """ numerics : numerics ',' int_number
                | numerics ',' float
                | int_number
                | float"""


#def p_numeric(p):
#    """ numeric : id
#               | float
#               | int"""


#tu jest shift reduce! dodanie ';' na końcu raz rozwiązało nie wiem czemu
def p_expression_binary_operators(p):
    """ expression : expression '+' expression
                   | expression '-' expression
                   | expression '/' expression
                   | expression '*' expression """
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
    """instruction : lvalue '=' expression ';'
                  | lvalue ADDASSIGN expression ';'
                  | lvalue SUBASSIGN expression ';'
                  | lvalue MULASSIGN expression ';'
                  | lvalue DIVASSIGN expression ';'"""


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
                   | PRINT expression"""


def p_key_phrases(p):
    """ expression : BREAK
                   | CONTINUE
                   | COMMENT
                   | RETURN expression"""


parser = yacc.yacc()
