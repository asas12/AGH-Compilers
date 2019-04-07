#!/usr/bin/python

import AST
import scanner
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    ('nonassoc', 'RETURN'),
    ('nonassoc', 'IF_NELSE'),
    ('nonassoc', 'ELSE'),
    ('nonassoc', 'ID'),
    ('nonassoc', 'PRINT'),
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
    p[0] = AST.Node("program", [p[1]])


def p_instructions_opt_1(p):
    """instructions_opt : instructions """
    p[0] = AST.Node("instructions_opt", [p[1]])


def p_instructions_opt_2(p):
    """instructions_opt : """
    p[0] = AST.Node("instructions_opt_none")


def p_instructions_1(p):
    """instructions : instructions instruction """
    p[0] = AST.Node("instructions", [p[1], p[2]])


def p_instructions_2(p):
    """instructions : instruction """
    p[0] = AST.Node("instruction", [p[1]])


# shift/reduce conflicts are resolved as shifts, which is correct
def p_instruction_expression(p):
    """instruction : instruction_simple ';' """
    p[0] = AST.Node("instruction_simple", [p[1]])


def p_instruction_if(p):
    """instruction : IF '(' condition ')' instruction %prec IF_NELSE"""
    p[0] = AST.Node("if", [p[3]], p[1])


def p_instruction_if_else(p):
    """instruction : IF '(' condition ')' instruction ELSE instruction"""
    p[0] = AST.If_Else([p[3]], [p[5]], [p[7]])


def p_instruction_for(p):
    """instruction : FOR id '=' expression ':' expression instruction"""
    p[0] = AST.For(p[2], p[4], p[6], [p[7]])


def p_instruction_while(p):
    """instruction : WHILE '(' condition ')' instruction"""
    p[0] = AST.Node("while", [p[3], p[5]], p[1])


def p_instruction_complex(p):
    """instruction : '{' instructions '}' """
    p[0] = AST.Node("complex_instructions", [p[2]])


def p_assign(p):
    """instruction_simple : lvalue '=' expression
                  | lvalue ADDASSIGN expression
                  | lvalue SUBASSIGN expression
                  | lvalue MULASSIGN expression
                  | lvalue DIVASSIGN expression """
    p[0] = AST.Node("assign", [p[1],p[3]], p[2])


def p_key_phrases(p):
    """ instruction_simple : BREAK
                   | CONTINUE
                   | COMMENT
                   | RETURN expressions
                   | PRINT '(' expressions ')'
                   | PRINT expressions"""
    if 'print' in p:
        if '(' in p:
            p[0] = AST.Node("print_instruction", [p[3]], p[1])
        else:
            p[0] = AST.Node("print_instruction", [p[2]], p[1])
    else:
        if p[1] == 'return':
            p[0] = AST.Node("return", [p[2]], p[1])
        else:
            p[0] = AST.Node("key_phrase", value=p[1])


def p_condition(p):
    """condition : expression LESS_EQUAL expression
                 | expression GREATER_EQUAL expression
                 | expression NOT_EQUAL expression
                 | expression EQUAL expression
                 | expression '<' expression
                 | expression '>' expression"""
    p[0] = AST.Node("condition", [p[1],p[3]], p[2])


def p_expressions(p):
    """expressions : expressions ',' expression
                   | expression"""
    if ',' in p:
        p[0] = AST.Node("expressions", [p[1], p[3]])
    else:
        p[0] = AST.Node("expressions", [p[1]])


def p_numeric_expression(p):
    """expression : int
                  | float"""
    p[0] = AST.Node("number", [p[1]])


def p_expression_floatnum(p):
    """ float : FLOATNUM"""
    p[0] = AST.Node("floatnum", value=p[1])


def p_expression_intnum(p):
    """ int : INTNUM """
    p[0] = AST.Node("intnum", value=p[1])


def p_expression_lvalue(p):
    """ expression : lvalue
        lvalue : id
               | id_arr"""
    p[0] = AST.Node("lvalue", [p[1]])


def p_expression_id(p):
    """ id : ID """
    p[0] = AST.Node("id", value=p[1])


def p_expression_array_index(p):
    """id_arr : id '[' int_numbers ']' """
    p[0] = AST.Node("arr_ind", [p[1], p[3]], "REF")


# contains int numbers and ids - used for indexing
def p_int_numbers(p):
    """ int_numbers : int_numbers ',' int_number
                | int_number"""
    if ',' in p:
        p[0] = AST.Node("int_numbers", [p[1], p[3]])
    else:
        p[0] = AST.Node("int_numbers", [p[1]])


def p_number(p):
    """int_number : id
              | int"""
    p[0] = AST.Node("number", [p[1]])


def p_matrix_expression(p):
    """ expression : matrix"""
    p[0] = AST.Node("expr_matrix", [p[1]], "MATRIX")


def p_matrix(p):
    """matrix : '['  matrices ']'
                  | '[' vectors ']' """
    p[0] = AST.Node("matrix", [p[2]])


def p_matrices(p):
    """ matrices :  matrix  ',' matrices
                 | matrix """
    if ',' in p:
        p[0] = AST.Node("matrices", [p[1], p[3]])
    else:
        p[0] = AST.Node("matrix", [p[1]])


def p_vectors(p):
    """ vectors :  all_numbers ';' vectors
                | all_numbers"""
    if ';' in p:
        p[0] = AST.Vectors("vectors", [p[1], p[3]], "VECTOR")
    else:
        p[0] = AST.Node("vectors", [p[1]], "VECTOR")


def p_all_numbers(p):
    """ all_numbers : all_numbers ',' int_number
                | all_numbers ',' float
                | int_number
                | float"""
    if ',' in p:
        p[0] = AST.Node("numeric", [p[1], p[3]])
    else:
        p[0] = AST.Node("numeric", [p[1]])


def p_expression_binary_operators(p):
    """ expression : expression '+' expression
                   | expression '-' expression
                   | expression '/' expression
                   | expression '*' expression """
    p[0] = AST.Node("bin_op", [p[1], p[3]], p[2])


def p_dot_operators(p):
    """expression : expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression"""
    p[0] = AST.Node("dot_op", [p[1], p[3]], p[2])


def p_transpose(p):
    """ expression : expression TRANSPOSE """
    p[0] = AST.Node("transpose", [p[1]], p[2])


def p_negation(p):
    """expression : '-' expression %prec UMINUS"""
    p[0] = AST.Node("negation", [p[2]], p[1])


def p_string(p):
    """expression : STRING """
    p[0] = AST.Node("string", value=p[1])


def p_functions(p):
    """ expression : ZEROS '(' expression ')'
                   | ONES '(' expression ')'
                   | EYE '(' expression ')'"""
    p[0] = AST.Node("function", [p[3]], p[1])


parser = yacc.yacc()
