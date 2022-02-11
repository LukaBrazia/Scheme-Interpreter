import re
from select import select
import sys
import functions
from functions import Function


class Tokenizer:
    def __init__(self, text):
        self.str = text
    def get_tokens(self):
        def valid(type):
            def func(_, token):
                return (token, type)
            return func
        scanner = re.Scanner([
            ("\s", None), # Whitespace
            (";[^;\n]*", None), # Comments
            ("\"[^\"]*\"|\'[^\"]*\'", valid("string")),
            ("'\s*\(", valid("raw_list")),
            ("\(", valid("list")),
            ("\)", valid("endl")),
            ("-?[0-9]+", lambda _, tok : (int(tok), "int")),
            ("-?[0-9]+\.[0-9]*|-?[0-9]*\.[0-9]+", lambda _, tok : (float(tok), "float")),
            ("#T|#t", lambda _, tok : (True, "bool")),
            ("#F|#f", lambda _, tok : (False, "bool")),
            ("[\w\+\-\.\*/<=>!\?:\$%_&~\^]*[a-zA-Z\+\-\.\*/<=>!\?:\$%_&~\^][\w\+\-\.\*/<=>!\?:\$%_&~\^]*", valid("id")),
            (".*", valid("ERROR")) # Garbage 
        ])
        tokens, _ = scanner.scan(self.str)
        return tokens




class Interpreter:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.ids = {
            "+" : Function(sum),
            "-" : Function(functions.sub),
            "*" : Function(functions.mult),
            "/" : Function(functions.div),
            ""
        }
    def next(self):
        if self.token_index == len(self.tokens):
            return None
        tok = self.tokens[self.token_index]
        self.token_index += 1
        return tok
    def peek(self):
        if self.token_index == len(self.tokens):
            return None
        tok = self.tokens[self.token_index]
        return tok
    def exp(self):
        pass

    def get_expression(self):
        if self.peek()[1] == "list":
            return self.exp_list()
        elif self.peek()[1] == "raw_list":
            self.next()
            return self.raw_list()
        elif self.peek()[1] == "id":
            if self.peek()[0] in self.ids.keys():
                return self.ids[self.next[0]]
            else:
                print(self.next[0] + " not defined")
                exit()
        else:
            return self.next()[0]
        

    def exp_list(self):
        self.next()
        func = self.get_expression()
        if not isinstance(func, Function):
            print("Object not callable")
            exit()
        params = self.raw_list()
        return func.execute(params)

    def raw_list(self):
        elems = []
        while True:
            if self.peek() == None:
                print("Expected a )")
                exit()
            if self.peek()[1] == "endl":
                self.next()
                break
            elems.append(self.get_expression())
        return elems
            


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("ERROR: Incorrect number of command line arguments")
        exit()
    if len(sys.argv) == 2:
        file = None
        try:
            file = open(sys.argv[1], "r")
        except:
            print("ERROR: File does not exist")
            exit()
        str = file.read()
        tk = Tokenizer(str)
        tokens = tk.get_tokens()
        print(None == 1)
        file.close()