#!/usr/bin/python
import AST
from SymbolTable import *
from collections import defaultdict
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logger = logging.getLogger(__name__)

class AllowedOperations(object):

    numeric_operators = ['+', '-', '*', '/']
    matrix_operators = ['.+', '.-', '.*', './']
    logical_operators = ['<', '>', '<=', '>=', '!=', '==']

    def __init__(self):
        self.allowed_opts = defaultdict(lambda: defaultdict(dict))

        self.allowed_opts['+']['int']['float'] = 'float'
        self.allowed_opts['*']['int']['float'] = 'float'

    def get_type(self, key1, key2, key3):
        if (key1 in self.allowed_opts) & (key2 in self.allowed_opts[key1]) & (key3 in self.allowed_opts[key1][key2]):
            return self.allowed_opts[key1][key2][key3]
        return False


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        # Called if no explicit visitor function exists for a node.
        print("Gen visit: "+ node.__class__.__name__ + ": "+str(node))
        #if isinstance(node, list):
        #    for elem in node:
        #        self.visit(elem)
        #else:
        #    for child in node.children:
        #        if isinstance(child, list):
        #            for item in child:
        #                if isinstance(item, AST.Node):
        #                    self.visit(item)
        #        elif isinstance(child, AST.Node):
        #            self.visit(child)

    # simpler version of generic_visit, not so general
    #def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)


class TypeChecker(NodeVisitor):

    def __init__(self):
        self.table = SymbolTable(None, 'Program')
        self.a = AllowedOperations()

    def visit_Program(self, node):
        logger.debug("Visiting program")
        self.visit(node.instructions_opt)

    def visit_InstructionsOpt(self, node):
        if node.instructions is not None:
            self.visit(node.instructions)
        else:
            logger.info("No instructions in instructions opt.")

    def visit_Instructions(self, node):
        self.visit(node.instruction)
        if node.instructions is not None:
            self.visit(node.instructions)

    def visit_Instruction(self, node):
        self.visit(node.instruction)

    def visit_InstructionIf(self, node):
        self.visit(node.condition)
        self.visit(node.instruction)

    def visit_InstructionIfElse(self, node):
        self.visit(node.condition)
        self.visit(node.then_part)
        self.visit(node.else_part)

    def visit_For(self, node):
        self.visit(node.iterator)
        self.visit(node.range_start)
        self.visit(node.range_end)
        self.visit(node.instruction)

    def visit_While(self, node):
        self.visit(node.condition)
        self.visit(node.instruction)

    def visit_Assign(self, node):
        # TODO symbol table
        left_symbol = self.visit(node.left)
        op = node.op
        right_symbol = self.visit(node.right)
        if right_symbol is None:
            print("WRONG ASSIGNMENT: l: ", left_symbol, "op: \"", op, "\" r: ", right_symbol)
        else:
            #TODO jeśli można! - to przy innych
            left_symbol.type = right_symbol.type


        logger.debug(str(["l: ", left_symbol,"op: ",op, "r: ",right_symbol]))
        print("l: ", left_symbol,"op: ",op, "r: ",right_symbol)

    def visit_KeyPhrase(self, node):
        self.visit(node.word)
        if node.argument is not None:
            self.visit(node.argument)

    def visit_Condition(self, node):
        self.visit(node.left)
        self.visit(node.op)
        self.visit(node.right)

    def visit_Expressions(self, node):
        self.visit(node.expression)
        if node.expressions is not None:
            self.visit(node.expressions)

    def visit_NumericExpression(self, node):
        return self.visit(node.number)

    def visit_IntNum(self, node):
        logger.debug('int: ' + str(node.value))
        return VariableSymbol(None, 'int')

    def visit_FloatNum(self, node):
        return VariableSymbol(None, 'float')

    def visit_LValue(self, node):
        return self.visit(node.value)

    def visit_ID(self, node):
        logger.debug("ID: "+node.id)
        print("ID: " + node.id)
        ret = self.table.get(node.id)
        if ret is None:
            new_id_symbol = VariableSymbol(node.id, None)
            self.table.put(node.id, new_id_symbol)
            return new_id_symbol
        else:
            return ret

    def visit_ArrayIndes(self, node):
        self.visit(node.id)
        self.visit(node.numbers)

    def visit_IntNumbers(self, node):
        self.visit(node.number)
        if node.numbers is not None:
            self.visit(node.numbers)

    def visit_Number(self, node):
        self.visit(node.number)

    def visit_MatrixExpression(self, node):
        self.visit(node.matrix)

    def visit_Matrix(self, node):
        self.visit(node.elements)

    def visit_Matrices(self, node):
        self.visit(node.matrix)
        if node.matrices is not None:
            self.visit(node.matrices)

    def visit_Vectors(self, node):
        self.visit(node.vector)
        if node.vectors is not None:
            self.visit(node.vectors)

    def visit_AllNumbers(self, node):
        self.visit(node.number)
        if node.numbers is not None:
            self.visit(node.numbers)

    def visit_BinOp(self, node):
                                          # alternative usage,
                                          # requires definition of accept method in class Node
        type1 = self.visit(node.left)     # type1 = node.left.accept(self) 
        type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        op = node.op

    def visit_DotOp(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = self.visit(node.op)

    def visit_Transpose(self, node):
        self.visit(node.expression)

    def visit_Negation(self, node):
        self.visit(node.expression)

    def visit_String(self, node):
        return VariableSymbol(None, 'string')

    def visit_Function(self, node):
        # TODO trzeba zobaczyć jakie są argumenty i zwracać macierz tego rozmiaru
        print("FUN", node.function, node.argument.number.number.value)

        return VariableSymbol(None, 'fun')

    def visit_ArrayIndex(self, node):
        # TODO nie wiem jak i kiedy wnioskować,
        # na pewno nie zawsze się da...
        # returns type of elements in array
        return VariableSymbol(None, 'array_element')


    def get_symbol_table(self):
        return self.table
        
#a = AllowedOperations()

#if a.get_type('+', 'int', 'float'):
#    print(a.allowed_opts['+']['int']['float'])

#if a.get_type('+', 'int', 'int'):
#    print(a.allowed_opts['+']['int']['int'])
#else:
#    print("NO1")

#if a.get_type('+', 'int', 'int'):
#    print(a.allowed_opts['+']['int']['int'])
#else:
#    print("NO1")

#print(a.allowed_opts['+']['int']['float'])
#try:
#    print(a.allowed_opts['+']['float']['int'])
#except KeyError:
#    print(a.allowed_opts)