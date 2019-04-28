

class Node(object):
    pass


class Program(Node):
    def __init__(self, instructions_opt):
        self.instructions_opt = instructions_opt


class InstructionsOpt(Node):
    def __init__(self, instructions=None):
        self.instructions = instructions


class Instructions(Node):
    def __init__(self, instruction, instructions=None):
        self.instruction = instruction
        self.instructions = instructions


class Instruction(Node):
    def __init__(self, instruction):
        self.instruction = instruction


class InstructionIf(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class InstructionIfElse(Node):
    def __init__(self, condition, then_part, else_part):

        self.condition = condition
        self.then_part = then_part
        self.else_part = else_part

    def add_indent(self):
        self.indent += '| '
        for child in self.children_cond+self.children_then+self.children_else:
            child.add_indent()

    def remove_indent(self):
        self.indent = self.indent[:-2]
        for child in self.children_cond+self.children_then+self.children_else:
            child.remove_indent()


class For(Node):
    def __init__(self, iterator, range_start, range_end, instruction):
        self.iterator = iterator
        self.range_start = range_start
        self.range_end = range_end
        self.instruction = instruction

    def __repr__(self):
        c = str(self.indent) + '| '
        ret = str(self.indent) + 'FOR\n'+str(self.indent) + str(self.iterator)+c + \
              'RANGE\n'+c+str(self.range_start)+c+str(self.range_end)

        for child in self.children:
            ret += str(child)
        # children[-1] is the list of remaining vectors
        return ret


class While(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class Assign(Node):
    def __init__(self, left, op, right, line):
        self.left = left
        self.op = op
        self.right = right
        self.line = line


class KeyPhrase(Node):
    def __init__(self, word, line, argument=None):
        self.word = word
        self.line = line
        self.argument = argument


class Condition(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Expressions(Node):
    def __init__(self, expression, expressions=None):
        self.expression = expression
        self.expressions = expressions


class NumericExpression(Node):
    def __init__(self, number):
        self.number = number


class IntNum(Node):
    def __init__(self, value):
        self.value = value


    def add_indent(self):
        if not hasattr(self, 'indent'):
            self.indent = ""
        self.indent += '| '

    def remove_indent(self):
        self.indent = self.indent[:-2]


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class LValue(Node):
    def __init__(self, value):
        self.value = value


class ID(Node):
    def __init__(self, id, line):
        self.id = id
        self.line = line


class ArrayIndex(Node):
    def __init__(self, id, numbers, line):
        self.id = id
        self.numbers = numbers
        self.line = line


class IntNumbers(Node):
    def __init__(self, number, numbers=None):
        self.number = number
        self.numbers = numbers


class Number(Node):
    def __init__(self, number):
        self.number = number


class MatrixExpression(Node):
    def __init__(self, matrix):
        self.matrix = matrix


class Matrix(Node):
    def __init__(self, elements, line):
        self.elements = elements
        self.line = line


class Matrices(Node):
    def __init__(self, matrix, matrices=None):
        self.matrix = matrix
        self.matrices = matrices


class Vectors(Node):
    def __init__(self, vector, vectors=None):
        self.vector = vector
        self.vectors = vectors

    def __repr__(self):
        if self.value is not None:
            ret = str(self.indent) + str(self.value) + '\n'

            if self.children:
                for child in self.children[:-1]:
                    ret += str(child)
                # children[-1] is the list of remaining vectors
                self.children[-1].remove_indent()
                ret += str(self.children[-1])
            return ret
        else:
            return "ERROR"


class AllNumbers(Node):
    def __init__(self, number, numbers=None):
        self.number = number
        self.numbers = numbers


class BinOp(Node):
    def __init__(self, left, op, right, line):
        self.left = left
        self.op = op
        self.right = right
        self.line = line


class DotOp(Node):
    def __init__(self, left, op, right, line):
        self.left = left
        self.op = op
        self.right = right
        self.line = line


class Transpose(Node):
    def __init__(self, expression):
        self.expression = expression


class Negation(Node):
    def __init__(self, expression):
        self.expression = expression


class String(Node):
    def __init__(self, string):
        self.string = string


class Function(Node):
    # zeros, ones, eye
    def __init__(self, function, argument):
        self.function = function
        self.argument = argument

class Error(Node):
    def __init__(self):
        pass
