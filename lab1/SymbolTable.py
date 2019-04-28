#!/usr/bin/python
from collections import defaultdict


class Symbol(object):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Sym named "+str(self.name)


class VariableSymbol(Symbol):

    def __init__(self, name, type):
        super().__init__(name)
        self.type = type

    def __repr__(self):
        return "VarSym "+str(self.name)+", type "+str(self.type)


class ArraySymbol(VariableSymbol):

    def __init__(self, name, dimensions):
        super().__init__(name, 'array')

        # list of sizes in dimensions?
        self.dimensions = dimensions

    def __repr__(self):
        return "ArraySymbol "+str(self.name)+", sized "+str(self.dimensions)


class FunctionSymbol(Symbol):

    def __init__(self, name, args):
        super().__init__(name)
        self.args = args


class SymbolTable(object):

    def __init__(self, parent, name):  # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.table = dict()
    #

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        self.table[name] = symbol
    #

    def get(self, name):  # get variable symbol or fundef from <name> entry
        if name in self.table:
            return self.table[name]
        else:
            #print("NO ", name)
            return None
    #

    def getParentScope(self):
        return self.parent
    #

    def pushScope(self, name):
        pass
    #

    def popScope(self):
        pass
    #

    def show(self):
        print(self.table)


