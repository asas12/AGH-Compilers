from __future__ import print_function
import AST


def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print_with_indent(str(self.value), indent)

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print_with_indent(str(self.value), indent)

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        self.instructions_opt.printTree(indent)

    @addToClass(AST.InstructionsOpt)
    def printTree(self, indent=0):
        if self.instructions is not None:
            self.instructions.printTree(indent)

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        self.instruction.printTree(indent)
        if self.instructions is not None:
            self.instructions.printTree(indent)

    @addToClass(AST.Instruction)
    def printTree(self, indent=0):
        self.instruction.printTree(indent)

    @addToClass(AST.InstructionIf)
    def printTree(self, indent=0):
        print_with_indent('IF', indent)
        self.condition.printTree(indent+1)
        print_with_indent('THEN', indent)
        self.instruction.printTree(indent+1)

    @addToClass(AST.InstructionIfElse)
    def printTree(self, indent=0):
        print_with_indent('IF', indent)
        self.condition.printTree(indent+1)
        print_with_indent('THEN', indent)
        self.then_part.printTree(indent+1)
        print_with_indent('ELSE', indent)
        self.else_part.printTree(indent+1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        print_with_indent('FOR', indent)
        self.iterator.printTree(indent+1)
        print_with_indent('RANGE', indent)
        self.range_start.printTree(indent+2)
        self.range_end.printTree(indent+2)
        self.instruction.printTree(indent+1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        print_with_indent('WHILE', indent)
        self.condition.printTree(indent+1)
        self.instruction.printTree(indent+1)

    @addToClass(AST.Condition)
    @addToClass(AST.Assign)
    def printTree(self, indent=0):
        print_with_indent(self.op, indent)
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)

    @addToClass(AST.KeyPhrase)
    def printTree(self, indent=0):
        print_with_indent(self.word.upper(), indent)
        if self.argument is not None:
            self.argument.printTree(indent+1)

    @addToClass(AST.Expressions)
    def printTree(self, indent=0):
        self.expression.printTree(indent)
        if self.expressions is not None:
            self.expressions.printTree(indent)

    @addToClass(AST.NumericExpression)
    def printTree(self, indent=0):
        self.number.printTree(indent)

    @addToClass(AST.LValue)
    def printTree(self, indent=0):
        self.value.printTree(indent)

    @addToClass(AST.ID)
    def printTree(self, indent=0):
        print_with_indent(self.id, indent)

    @addToClass(AST.ArrayIndex)
    def printTree(self, indent=0):
        print_with_indent('REF', indent)
        self.id.printTree(indent+1)
        self.numbers.printTree(indent+1)

    @addToClass(AST.IntNumbers)
    def printTree(self, indent=0):
        self.number.printTree(indent)
        if self.numbers is not None:
            self.numbers.printTree(indent)

    @addToClass(AST.Number)
    def printTree(self, indent=0):
        self.number.printTree(indent)

    @addToClass(AST.MatrixExpression)
    def printTree(self, indent=0):
        print_with_indent('MATRIX', indent)
        self.matrix.printTree(indent+1)

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        self.elements.printTree(indent)

    @addToClass(AST.Matrices)
    def printTree(self, indent=0):
        self.matrix.printTree(indent)
        if self.matrices is not None:
            self.matrices.printTree(indent)

    @addToClass(AST.Vectors)
    def printTree(self, indent=0):
        print_with_indent('VECTOR', indent)
        self.vector.printTree(indent+1)
        if self.vectors is not None:
            self.vectors.printTree(indent+1)

    @addToClass(AST.AllNumbers)
    def printTree(self, indent=0):
        self.number.printTree(indent)
        if self.numbers is not None:
            self.numbers.printTree(indent)

    @addToClass(AST.BinOp)
    def printTree(self, indent=0):
        print_with_indent(self.op, indent)
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)

    @addToClass(AST.DotOp)
    def printTree(self, indent=0):
        print_with_indent(self.op, indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Negation)
    def printTree(self, indent=0):
        print_with_indent('-', indent)
        self.expression.printTree(indent+1)

    @addToClass(AST.Transpose)
    def printTree(self, indent=0):
        print_with_indent('TRANSPOSE', indent)
        self.expression.printTree(indent+1)

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print_with_indent(self.string, indent)


    @addToClass(AST.Function)
    def printTree(self, indent=0):
        print_with_indent(self.function, indent)
        self.argument.printTree(indent+1)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass


def print_with_indent(string, indent):
    print(indent*'| ' + string)
