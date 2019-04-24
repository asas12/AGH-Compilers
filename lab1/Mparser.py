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
    ('left', '<', '>', 'LESS_EQUAL', 'GREATER_EQUAL', 'NOT_EQUAL', 'EQUAL'),
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
    p[0] = AST.Program(p[1])


def p_instructions_opt_1(p):
    """instructions_opt : instructions """
    p[0] = AST.InstructionsOpt(p[1])


def p_instructions_opt_2(p):
    """instructions_opt : """
    p[0] = AST.InstructionsOpt()


def p_instructions_1(p):
    """instructions : instructions instruction """
    p[0] = AST.Instructions(p[1], p[2])


def p_instructions_2(p):
    """instructions : instruction """
    p[0] = AST.Instructions(p[1])


# shift/reduce conflicts are resolved as shifts, which is correct
def p_instruction_expression(p):
    """instruction : instruction_simple ';' """
    p[0] = AST.Instruction(p[1])


def p_instruction_if(p):
    """instruction : IF '(' condition ')' instruction %prec IF_NELSE"""
    p[0] = AST.InstructionIf(p[3], p[5])


def p_instruction_if_else(p):
    """instruction : IF '(' condition ')' instruction ELSE instruction"""
    p[0] = AST.InstructionIfElse(p[3], p[5], p[7])


def p_instruction_for(p):
    """instruction : FOR id '=' expression ':' expression instruction"""
    p[0] = AST.For(p[2], p[4], p[6], p[7])


def p_instruction_while(p):
    """instruction : WHILE '(' condition ')' instruction"""
    p[0] = AST.While(p[3], p[5])


def p_instruction_complex(p):
    """instruction : '{' instructions '}' """
    p[0] = AST.Instruction(p[2])


def p_assign(p):
    """instruction_simple : lvalue '=' expression
                  | lvalue ADDASSIGN expression
                  | lvalue SUBASSIGN expression
                  | lvalue MULASSIGN expression
                  | lvalue DIVASSIGN expression """
    p[0] = AST.Assign(p[1], p[2], p[3])


def p_key_phrases(p):
    """ instruction_simple : BREAK
                   | CONTINUE
                   | COMMENT
                   | RETURN expressions
                   | PRINT '(' expressions ')'
                   | PRINT expressions"""
    if 'print' in p:
        if '(' in p:
            p[0] = AST.KeyPhrase(p[1], p[3])
        else:
            p[0] = AST.KeyPhrase(p[1], p[2])
    else:
        if p[1] == 'return':
            p[0] = AST.KeyPhrase(p[1], p[2])
        else:
            p[0] = AST.KeyPhrase(p[1])


def p_condition(p):
    """condition : expression LESS_EQUAL expression
                 | expression GREATER_EQUAL expression
                 | expression NOT_EQUAL expression
                 | expression EQUAL expression
                 | expression '<' expression
                 | expression '>' expression"""
    p[0] = AST.Condition(p[1], p[2], p[3])


def p_expressions(p):
    """expressions : expressions ',' expression
                   | expression"""
    if ',' in p:
        p[0] = AST.Expressions(p[3], p[1])
    else:
        p[0] = AST.Expressions(p[1])


def p_numeric_expression(p):
    """expression : int
                  | float"""
    p[0] = AST.NumericExpression(p[1])


def p_expression_floatnum(p):
    """ float : FLOATNUM"""
    p[0] = AST.FloatNum(p[1])


def p_expression_intnum(p):
    """ int : INTNUM """
    p[0] = AST.IntNum(value=p[1])


def p_expression_lvalue(p):
    """ expression : lvalue
        lvalue : id
               | id_arr"""
    p[0] = AST.LValue(p[1])


def p_expression_id(p):
    """ id : ID """
    p[0] = AST.ID(p[1])


def p_expression_array_index(p):
    """id_arr : id '[' int_numbers ']' """
    p[0] = AST.ArrayIndex(p[1], p[3])


# contains int numbers and ids - used for indexing
def p_int_numbers(p):
    """ int_numbers : int_numbers ',' int_number
                | int_number"""
    if ',' in p:
        p[0] = AST.IntNumbers(p[3], p[1])
    else:
        p[0] = AST.IntNumbers(p[1])


def p_number(p):
    """int_number : id
              | int"""
    p[0] = AST.Number(p[1])


def p_matrix_expression(p):
    """ expression : matrix"""
    p[0] = AST.MatrixExpression(p[1])


def p_matrix(p):
    """matrix : '['  matrices ']'
                  | '[' vectors ']' """
    p[0] = AST.Matrix(p[2])


def p_matrices(p):
    """ matrices :  matrix  ',' matrices
                 | matrix """
    if ',' in p:
        p[0] = AST.Matrices(p[1], p[3])
    else:
        p[0] = AST.Matrices(p[1])


def p_vectors(p):
    """ vectors :  all_numbers ';' vectors
                | all_numbers"""
    if ';' in p:
        p[0] = AST.Vectors(p[1], p[3])
    else:
        p[0] = AST.Vectors(p[1])


def p_all_numbers(p):
    """ all_numbers : all_numbers ',' int_number
                | all_numbers ',' float
                | int_number
                | float"""
    if ',' in p:
        p[0] = AST.AllNumbers(p[3], p[1])
    else:
        p[0] = AST.AllNumbers(p[1])


def p_expression_binary_operators(p):
    """ expression : expression '+' expression
                   | expression '-' expression
                   | expression '/' expression
                   | expression '*' expression """
    p[0] = AST.BinOp(p[1], p[2], p[3])


def p_dot_operators(p):
    """expression : expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression"""
    p[0] = AST.DotOp(p[1], p[2], p[3])


def p_transpose(p):
    """ expression : expression TRANSPOSE """
    p[0] = AST.Transpose(p[1])


def p_negation(p):
    """expression : '-' expression %prec UMINUS"""
    p[0] = AST.Negation(p[2])


def p_string(p):
    """expression : STRING """
    p[0] = AST.String(p[1])


def p_functions(p):
    """ expression : ZEROS '(' expression ')'
                   | ONES '(' expression ')'
                   | EYE '(' expression ')'"""
    p[0] = AST.Function(p[1], p[3])


parser = yacc.yacc()
