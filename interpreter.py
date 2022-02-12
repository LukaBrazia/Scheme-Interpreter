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
            ("'\s*\(", valid("raw_list")),
            ("\(", valid("list")),
            ("\"[^\"]*\"|\'[^\"]*\'", valid("string")),
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
            "and": Function(functions.andexp),
            "or" : Function(functions.orexp),
            "cdr": Function(functions.cdr),
            "car": Function(functions.car),
            "cons": Function(functions.cons),
            "append": Function(functions.append),
            "map": Function(functions.mapexp),
            "apply" : Function(functions.apply),
            "eval" : Function(functions.eval)
        }

    def execute(self, type):
        return self.exp_list()

    def expect(self, st):
        print("Was expecting a " + st)
        exit()

    def interpret_body(self, cli):
        while self.token_index != len(tokens):
            if self.peek()[1] == "raw_list":
                self.next()
                message = self.raw_list()
                if cli and message is not None: print(message)
            elif self.peek()[1] == "list":
                self.next()
                if self.peek()[0] == "define":
                    self.next()
                    if (self.peek()[1] == "list"):
                        self.next()
                        name = self.next()
                        if name[1] != "id":
                            print("Expected an id")
                            exit()
                        self.ids[name[0]] = Function(self.createFunc())
                        self.next()
                    else:
                        self.createVar()
                else:
                    message = self.exp_list()
                    if cli and message is not None: print(message)
            else:
                print(self.peek())
                print("Expected a list")
                exit()

    def createVar(self):
        if self.peek()[1] != "id":
            print("Expected an ID")
            exit()
        name = self.next()[0]
        val = self.get_expression()
        if self.peek()[1] != "endl":
            print("Expected a )")
            exit()
        self.next()
        self.ids[name] = val


    def createFunc(self):
        params = {}
        ind = 0
        while self.peek()[1] != "endl":
            if self.peek() == None:
                print("Expected a )")
                exit()
            params[(self.next()[0])] = ind
            ind += 1
        self.next()
        self.next() 
        funcTokens = []
        while self.peek()[1] != "endl":
            if self.peek() == None:
                print("Expected a )")
                exit()
            funcTokens.append(self.next())
        funcTokens.append(self.next())
        def func(args):
            tempTokens = []
            for tok in funcTokens:
                if tok[0] in params.keys():
                    tempTokens.append((args[params[tok[0]]], ""))
                else:
                    tempTokens.append(tok)
            inp = Interpreter(tempTokens)
            inp.ids = self.ids
            return inp.exp_list()
        return func
            

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
            self.next()
            return self.exp_list()
        elif self.peek()[1] == "raw_list":
            self.next()
            return self.raw_list()
        elif self.peek()[1] == "id":
            if self.peek()[0] in self.ids.keys():
                return self.ids[self.next()[0]]
            elif self.peek()[0] == "lambda":
                self.next()
                self.next()
                func = Function(self.createFunc())
                return Function(lambda _ : func)
            else:
                print(self.next[0] + " not defined")
                exit()
        else:
            return self.next()[0]
        

    def exp_list(self):
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
        inp = Interpreter(tokens)
        inp.interpret_body(True)
        file.close()