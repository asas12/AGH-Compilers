class Node(object):
    def __init__(self, type, children=None, value=None, indent=''):
        self.type = type
        self.indent = indent
        self.value = value

        if children:
            self.children = children
            if value:
                for child in children:
                    child.add_indent()
        else:
            self.children = []

    def __repr__(self):
        if self.value is not None:
            ret = str(self.indent) + str(self.value) + '\n'

            if self.children:
                for child in self.children:
                    ret += str(child)
            return ret
        else:
            ret = ""
            if self.children:
                for child in self.children:
                    ret += str(child)
            return ret

    def add_indent(self):
        self.indent += '| '
        for child in self.children:
            child.add_indent()

    def remove_indent(self):
        self.indent = self.indent[:-2]
        for child in self.children:
            child.remove_indent()


class Vectors(Node):
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


class If_Else(Node):
    def __init__(self, children_cond=None, children_then=None, children_else=None, indent=''):
        self.indent = indent

        if children_cond:
            self.children_cond = children_cond
            for child in children_cond:
                    # child.indent += self.indent + '|'
                    child.add_indent()
        else:
            self.children_cond = []

        if children_then:
            self.children_then = children_then
            for child in children_then:
                    # child.indent += self.indent + '|'
                    child.add_indent()
        else:
            self.children_then = []

        if children_else:
            self.children_else = children_else
            for child in children_else:
                # child.indent += self.indent + '|'
                child.add_indent()
        else:
            self.children_else = []

    def add_indent(self):
        self.indent += '| '
        for child in self.children_cond+self.children_then+self.children_else:
            child.add_indent()

    def remove_indent(self):
        self.indent = self.indent[:-2]
        for child in self.children_cond+self.children_then+self.children_else:
            child.remove_indent()

    def __repr__(self):
        ret = str(self.indent) + 'IF\n'
        for child in self.children_cond:
            ret += str(child)

        ret += str(self.indent) + 'THEN\n'
        for child in self.children_then:
            ret += str(child)

        ret += str(self.indent) + 'ELSE\n'
        for child in self.children_else:
            ret += str(child)
        # children[-1] is the list of remaining vectors
        return ret


class For(Node):
    def __init__(self, iterator=None, range_start=None, range_end=None, children=None, indent=''):
        self.indent = indent
        self.iterator = iterator
        iterator.add_indent()
        self.range_start = range_start
        self.range_end = range_end
        self.range_end.add_indent()
        self.range_start.add_indent()

        if children:
            self.children = children
            for child in children:
                child.add_indent()
        else:
            self.children = []

    def __repr__(self):
        c = str(self.indent) + '| '
        ret = str(self.indent) + 'FOR\n'+str(self.indent) + str(self.iterator)+c + \
              'RANGE\n'+c+str(self.range_start)+c+str(self.range_end)

        for child in self.children:
            ret += str(child)
        # children[-1] is the list of remaining vectors
        return ret
