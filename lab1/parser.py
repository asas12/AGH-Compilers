import sys
from lexer import scanner
import Mparser
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example_full.txt"
        file = open(filename, "r")
        print('Parsing: ', filename)
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()
    parser.text = text
    ast = parser.parse(text, lexer=scanner.lexer)
    #print(p)
    ast.printTree()

    # Below code shows how to use visitor
    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    typeChecker.get_symbol_table().show()
    # or alternatively ast.accept(typeChecker)