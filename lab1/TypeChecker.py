#!/usr/bin/python
import AST
from SymbolTable import *
from collections import defaultdict
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logger = logging.getLogger(__name__)


class AllowedOperations(object):
    # This class doesn't check matrix dimensions

    types = ['int', 'float', 'string', 'array']
    numeric_types = ['int', 'float']
    numeric_operators_with_div = ['+', '-', '*', '/']
    numeric_operators = ['+', '-', '*']
    div_operator = ['/']
    dot_operators = ['.+', '.-', '.*', './']
    logical_operators = ['<', '>', '<=', '>=', '!=', '==']
    equal_operators = ['!=', '==']
    assign_operators = ['+=', '-=', '*=', '/=']

    def __init__(self):
        self.allowed_opts = defaultdict(lambda: defaultdict(dict))

        # +, -, * will give type for both arguments of the same given type
        for operator in self.numeric_operators:
            for type in self.types:
                self.allowed_opts[operator][type][type] = type

        # float makes float out of all numeric operations
        for operator in self.numeric_operators_with_div:
            for type1 in self.numeric_types:
                self.allowed_opts[operator][type1]['float'] = 'float'
                self.allowed_opts[operator]['float'][type1] = 'float'

        # division gives float for numeric types
        for type in self.numeric_types:
            self.allowed_opts['/'][type][type] = 'float'

        # string operations
        self.allowed_opts['+']['string']['string'] = 'string'
        self.allowed_opts['*']['int']['string'] = 'string'
        self.allowed_opts['*']['string']['int'] = 'string'
        self.allowed_opts['+=']['string']['string'] = 'string'

        # dot operators
        for operator in self.dot_operators:
            self.allowed_opts[operator]['array']['array'] = 'array'

        # int for logical
        # all can be checked for equality
        for operator in self.equal_operators:
            for type1 in self.types:
                    self.allowed_opts[operator][type1][type1] = 'int'
            self.allowed_opts[operator]['int']['float'] = 'int'
            self.allowed_opts[operator]['float']['int'] = 'int'

        # int and float and None can be compared in all ways
        for operator in self.logical_operators:
            for type1 in self.numeric_types+[None]:
                for type2 in self.numeric_types+[None]:
                    self.allowed_opts[operator][type1][type2] = 'int'

        # assignments simple
        for type1 in self.types:
            for type2 in self.types:
                self.allowed_opts['='][type1][type2] = type2
                self.allowed_opts['='][None][type2] = type2

        # -=, +=, *=, /= gives float when second is float
        for operator in self.assign_operators:
            for type1 in self.numeric_types:
                for type2 in self.numeric_types:
                    self.allowed_opts[operator][type1][type2] = 'float'

        for operator in self.assign_operators:
            self.allowed_opts[operator]['array']['array'] = 'array'

    def get_type_from_symbols(self, op, left, right):
        if (op in self.allowed_opts) and (left.type in self.allowed_opts[op]) and \
                (right.type in self.allowed_opts[op][left.type]):
            return self.allowed_opts[op][left.type][right.type]
        return None

    def get_type_from_types(self, op, left_type, right_type):
        if (op in self.allowed_opts) and (left_type in self.allowed_opts[op]) and \
                (right_type in self.allowed_opts[op][left_type]):
            return self.allowed_opts[op][left_type][right_type]
        return None

    def new_array_dimensions(self, op, left_symbol, right_symbol):
        if op == '=':
            #print("HERE",op, left_symbol, right_symbol)
            return right_symbol.dimensions
        if op in ['+', '-', '-=','+='] + self.dot_operators + self.assign_operators:
            if left_symbol.dimensions == right_symbol.dimensions:
                return left_symbol.dimensions
        if op == '*':
            if left_symbol.dimensions[1] == right_symbol.dimensions[0]:
                return [left_symbol.dimensions[0], right_symbol.dimensions[1]]
        if op == '/':
            return [left_symbol.dimensions[0], right_symbol.dimensions[1]]
        #print("NONE")
        return None

    def __str__(self):
        ret = ''
        for op in self.allowed_opts:
            for type1 in self.allowed_opts[op]:
                for type2 in self.allowed_opts[op][type1]:
                    t = self.get_type_from_types(op, type1, type2)
                    if t is not None:
                        ret += (op+"\t"+str(type1)+"\t"+str(type2))+":\t"+str(t)+'\n'
        return ret


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
        self.in_loop = 0

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
        self.in_loop += 1
        self.visit(node.instruction)
        self.in_loop -= 1

    def visit_While(self, node):
        self.visit(node.condition)
        self.in_loop += 1
        self.visit(node.instruction)
        self.in_loop -= 1

    def visit_Assign(self, node):
        left_symbol = self.visit(node.left)
        op = node.op
        right_symbol = self.visit(node.right)

        type = self.a.get_type_from_symbols(op, left_symbol, right_symbol)
        if type is not None:
            # right hand side equals to something
            if type is 'array':
                # assigning an array, check if it is legal
                new_dim = self.a.new_array_dimensions(op, left_symbol, right_symbol)
                if new_dim is not None:
                    print("Line ", node.line, " array assignment l: ", left_symbol, "op: ", op, "r: ", right_symbol)
                    self.table.put(left_symbol.name, ArraySymbol(left_symbol.name, right_symbol.dimensions))
                else:
                    print("Line ", node.line, "! wrong array assignment: l: ", left_symbol, "op: \"", op, "\" r: ",
                          right_symbol)
            else:
                # assigning variable, not an array
                print("Line ", node.line, " assignment l: ", left_symbol, "op: ", op, "r: ", right_symbol)
                self.table.put(left_symbol.name, VariableSymbol(left_symbol.name, right_symbol.type))
        else:
            # right hand side is wrong, cannot assign
            print("Line ", node.line, "! wrong assignment: l: ", left_symbol, "op: \"", op, "\" r: ", right_symbol)

        logger.debug(str(["l: ", left_symbol,"op: ",op, "r: ",right_symbol]))

    def visit_KeyPhrase(self, node):
        if (node.word == 'continue' or node.word == 'break') and not self.in_loop>0:
            print("Line ", node.line, "! BREAK or CONTINUE outside a loop")
        else:
            # self.visit(node.word)
            if node.argument is not None:
                self.visit(node.argument)

    def visit_Condition(self, node):
        sym_left = self.visit(node.left)
        op = node.op
        sym_right = self.visit(node.right)
        new_type = self.a.get_type_from_symbols(op, sym_left, sym_right)

        if new_type != 'int':
            print(new_type, op, sym_left, sym_right)

            print("Wrong condition")
        #return VariableSymbol(None, 'int')

    def visit_Expressions(self, node):
        #
        self.visit(node.expression)
        if node.expressions is not None:
            self.visit(node.expressions)

    def visit_NumericExpression(self, node):
        return self.visit(node.number)

    def visit_IntNum(self, node):
        logger.debug('int: ' + str(node.value))
        #print('int', node.value)
        return VariableSymbol(None, 'int')

    def visit_FloatNum(self, node):
        return VariableSymbol(None, 'float')

    def visit_LValue(self, node):
        return self.visit(node.value)

    def visit_ID(self, node):
        logger.debug("ID: "+node.id)
        #print("ID: " + node.id + " " + str(node.line))
        ret = self.table.get(node.id)
        #print(ret)
        if ret is None:
            new_id_symbol = VariableSymbol(node.id, None)
            self.table.put(node.id, new_id_symbol)
            return new_id_symbol
        else:
            return ret

    def visit_Number(self, node):
        return self.visit(node.number)

    def visit_MatrixExpression(self, node):
        return self.visit(node.matrix)

    def visit_Matrix(self, node):
        #print("MATRIX")
        vector = self.visit(node.elements)
        # unpacking vectors to check sizes... not so great
        while isinstance(vector.dimensions[0], ArraySymbol):
            for i, dim in enumerate(vector.dimensions):
                vector.dimensions[i] = dim.dimensions
        if all(dim == vector.dimensions[0] for dim in vector.dimensions):
            return vector
        else:
            if vector.name is not None:
                print("Line ", node.line, "! wrong dimensions in ", vector.name)
            else:
                print("Line ", node.line, "! wrong dimensions in unnamed vector.", vector.dimensions)
        return ArraySymbol(None, None)

    def visit_IntNumbers(self, node):
        #print("INTNUMBERS")
        self.visit(node.number)
        if node.numbers is not None:
            self.visit(node.numbers)

    def visit_Matrices(self, node):
        #print("MATRICES")
        if node.matrices is not None:
            return ArraySymbol(None, [self.visit(node.matrix)]+self.visit(node.matrices).dimensions)
        return ArraySymbol(None, [self.visit(node.matrix)])

    def visit_Vectors(self, node):
        #print("VECTORS")
        if node.vectors is not None:
            return ArraySymbol(None, [self.visit(node.vector)] + self.visit(node.vectors).dimensions)
        else:
            return ArraySymbol(None, [self.visit(node.vector)])

    def visit_AllNumbers(self, node):
        # returns size of the vector
        if node.numbers is not None:
            return 1 + self.visit(node.numbers)
        return 1


    def visit_BinOp(self, node):
                                          # alternative usage,
                                          # requires definition of accept method in class Node
        left_symbol = self.visit(node.left)     # type1 = node.left.accept(self)
        right_symbol = self.visit(node.right)    # type2 = node.right.accept(self)
        op = node.op

        return_type = self.a.get_type_from_symbols(op, left_symbol, right_symbol)
        if return_type is 'array':
            new_dim = self.a.new_array_dimensions(op, left_symbol, right_symbol)
            if new_dim is None:
                print("Line ", node.line, "! wrong array binop: ", op, " left: ", left_symbol, "right: ", right_symbol)
                return ArraySymbol(None, None)
            else:
                return ArraySymbol(None, new_dim)

        if return_type is None:
            print("Line ", node.line,"! wrong binop: ",op, " left: ",left_symbol, "right: ", right_symbol)
        #print("BINOP", return_type)

        return VariableSymbol(None, return_type)

    def visit_DotOp(self, node):
        left_symbol = self.visit(node.left)
        right_symbol = self.visit(node.right)
        op = node.op
        #op = self.visit(node.op)
        return_type = self.a.get_type_from_symbols(op, left_symbol, right_symbol)
        if return_type is 'array':
            new_dim = self.a.new_array_dimensions(op, left_symbol, right_symbol)
            if new_dim is None:
                print("Line ", node.line, "! wrong dotop: ", op, " left: ", left_symbol, "right: ", right_symbol)
                return ArraySymbol(None, None)
            else:
                return ArraySymbol(None, new_dim)

        if return_type is None:
            print("Line ", node.line, "! wrong dotop: ", op, " left: ", left_symbol, "right: ", right_symbol)
        # print("DotOp", return_type)

        return VariableSymbol(None, return_type)

    def visit_Transpose(self, node):
        # TODO change sizes? check if matrix
        return self.visit(node.expression)

    def visit_Negation(self, node):
        # TODO check if can be negated?
        return self.visit(node.expression)

    def visit_String(self, node):
        return VariableSymbol(None, 'string')

    def visit_Function(self, node):
        #print("FUN", node.function, node.argument.number.number.value)

        args = get_matrix_size(node.argument)
        #print("ARGS: ", args)
        return ArraySymbol(None, args)

    def visit_ArrayIndex(self, node):
        # TODO nie wiem jak i kiedy wnioskować,
        # na pewno nie zawsze się da...
        # returns type of elements in array
        array_symbol = self.table.get(node.id.id)
        if array_symbol is not None:
            if array_symbol.type != 'array':
                print("Line ", node.line, ": ", node.id.id, "! is not an array!")
                return VariableSymbol(None, None)
            else:
                size = []
                append_int_numbers_to_list(node.numbers, size)
                if len(size) != len(array_symbol.dimensions):
                    print("Line ", node.line, "! wrong dimensions in", node.id.id)
                    return VariableSymbol(None, None)
                elif not all(a<b for a, b in zip(size, array_symbol.dimensions)):
                    print("Line ", node.line, "! out of bounds in", node.id.id)
                    return VariableSymbol(None, None)
        else:
            print("Line ", node.line, "! no such array: ", node.id.id)
            return VariableSymbol(None, None)
        return VariableSymbol(None, 'float')

    def get_symbol_table(self):
        return self.table


def get_matrix_dimensions(args):
    if args.numbers is None:
        return 1
    else:
        return 1 + get_matrix_dimensions(args.numbers)


def get_matrix_size(args):
    ret = []
    append_int_numbers_to_list(args, ret)
    return ret


def append_int_numbers_to_list(int_numbers, list):
    list.append(int_numbers.number.number.value)
    if int_numbers.numbers is not None:
        append_int_numbers_to_list(int_numbers.numbers, list)
