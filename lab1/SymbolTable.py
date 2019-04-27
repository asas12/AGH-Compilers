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
        return "Var Sym "+str(self.name)+", type "+str(self.type)


class ArraySymbol(Symbol):

    def __init__(self, name, size):
        super().__init__(name)

        # list of sizes in dimensions?
        self.size = size

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
            return None
    #

    def getParentScope(self):
        pass
    #

    def pushScope(self, name):
        pass
    #

    def popScope(self):
        pass
    #

    def show(self):
        print(self.table)


