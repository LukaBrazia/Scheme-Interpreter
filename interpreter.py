import re
import sys
import functions
from functions import Function, kawaPrint
from collections.abc import Hashable

class Tokenizer:
    def __init__(self, text):
        self.str = text
    def get_tokens(self):
        def valid(type):
            def func(_, token):
                return (token, type)
            return func
        def string(_, token):
            return (token[1:-1], "string")

        scanner = re.Scanner([
            ("\s", None), # Whitespace
            (";[^;\n]*", None), # Comments
            ("'\s*\(", valid("raw_list")),
            ("\(", valid("list")),
            ("\"[^\"]*\"|\'[^\"]*\'", string),
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
            "eval" : Function(functions.eval),
            "display" : Function(functions.display),
            "null?" : Function(functions.null),
            "length" : Function(functions.length),
            "=" : Function(functions.num_eq),
            "<" : Function(functions.num_lt),
            "<=" : Function(functions.num_le),
            ">" : Function(functions.num_gt),
            ">=" : Function(functions.num_ge),
            "equal?" : Function(functions.equal),
            "zero?" : Function(functions.zero),
            "remainder" : Function(functions.remainder),
            "quotient" : Function(functions.quotient),
            "newline" : Function(functions.newline),
            "list" : Function(functions.ls),
            "positive?" : Function(functions.positive),
            "negative?" : Function(functions.negative),
            "odd?" : Function(functions.odd),
            "even?" : Function(functions.even),
            "expt" : Function(functions.expt),
            "sqrt" : Function(functions.sqrt),
            "reverse" : Function(functions.reverse),
            "not" : Function(functions.notexp),
            "else" : True
        }        
        self.generate(functions.car, "a")
        self.generate(functions.cdr, "d")

    def generate(self, func, str):
        if len(str) == 10:
            return
        str1 = "a" + str
        func1 = lambda params: functions.car([func(params)])
        self.ids["c" + str1 + "r"] = Function(func1)
        self.generate(func1, str1)
        str2 = "d" + str
        func2 = lambda params: functions.cdr([func(params)])
        self.ids["c" + str2 + "r"] = Function(func2)
        self.generate(func2, str2)

    def execute(self, type):
        return self.exp_list()

    def expect(self, st):
        print("Was expecting a " + st)
        exit()

    def interpret_body(self, cli):
        while self.token_index != len(tokens):
            if (self.peek() == None):
                break
            if self.peek()[1] == "raw_list":
                self.next()
                message = self.raw_list()
                if cli and message is not None: print(kawaPrint(message))
            elif self.peek()[1] == "list":
                self.next()
                if self.peek()[0] == "define":
                    self.next()
                    if (self.peek()[1] == "list"):
                        self.next()
                        name = self.next()
                        if name[1] != "id":
                            print("Expected a function name in define")
                            exit()
                        self.ids[name[0]] = Function(self.createFunc())
                        self.next()
                    else:
                        self.createVar()
                elif self.peek()[0] == "load":
                    self.next()
                    if (self.peek()[1] != "string"):
                        print("Expected a filename in load")
                        exit()
                    filename = self.next()[0]
                    self.next()
                    file = None
                    try:
                        file = open(filename, "r", encoding="utf-8")
                    except:
                        print("ERROR: File does not exist")
                        exit()
                    str = file.read()
                    tk = Tokenizer(str)
                    newtokens = tk.get_tokens()
                    self.tokens = self.tokens[:self.token_index] + newtokens + self.tokens[self.token_index:]
                else:
                    message = self.exp_list()
                    if cli and message is not None: print(kawaPrint(message))
            else:
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
        return name

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
        brackets = 1
        while brackets != 0:
            if self.peek() == None:
                print("Expected a )")
                exit()
            elif self.peek()[1] in ("list", "raw_list"):
                brackets += 1
            elif self.peek()[1] == "endl":
                brackets -= 1
            funcTokens.append(self.next())
        def func(args):
            if (len(args) != len(params)):
                print("Incorrect number of aruments in function call")
                exit()
            tempTokens = []
            for tok in funcTokens:
                if isinstance(tok[0], Hashable) and tok[0] in params.keys():
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

    def skip_exp(self):
        if self.peek()[1] in ("list", "raw_list"):
            self.next()
            while self.peek()[1] != "endl":
                self.skip_exp()
            self.next()
        elif self.peek()[1] != "endl":
            self.next()
        else: 
            return False
        return True

    def get_if(self):
        exp = self.get_expression()
        val = None
        if exp:
            val = self.get_expression()
            self.skip_exp()
        else:
            self.skip_exp()
            if self.peek()[1] != "endl":
                val = self.get_expression()
        return Function(lambda _ : val)

    

    def get_cond_st(self):
        exp = self.get_expression()
        val = None
        if self.peek()[1] == "endl":
            return Function(lambda _: exp)
        if exp:
            val = self.get_expression()
            self.skip_exp()
            return Function(lambda _ : val)
        else:
            self.skip_exp()
    
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
            elif self.peek()[0] == "if":
                self.next()
                return self.get_if()
            elif self.peek()[0] == "cond":
                self.next()
                val = None
                while self.peek()[1] != "endl":
                    if self.peek()[1] != "list":
                        print("Unexpected token in cond")
                        exit()
                    if val == None:
                        self.next()
                        val = self.get_cond_st()
                        if self.peek()[1] != "endl":
                            print("Unexpected token in cond")
                            exit()
                        self.next()
                    else:
                        self.skip_exp()
                if val == None:
                    return Function(lambda x : None)
                return val
            elif self.peek()[0] == "let":
                self.next()
                if self.next()[1] != "list":
                    print("Expected a list of variables")
                    exit()
                params = []
                while self.peek()[1] != "endl":
                    if self.next()[1] != "list":
                        print("Expected a list of variables")
                        exit()
                    params.append(self.createVar())
                
                self.next()
                exp = self.get_expression()
                for param in params:
                    self.ids.pop(param)
                return Function(lambda x : exp)
                    
            else:
                print(self.peek())
                print("ID not defined")
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
            file = open(sys.argv[1], "r", encoding="utf-8")
        except:
            print("ERROR: File does not exist")
            exit()
        str = file.read()
        tk = Tokenizer(str)
        tokens = tk.get_tokens()
        inp = Interpreter(tokens)
        inp.interpret_body(False) #set to true if testing
        file.close()
    else:
        linenum = 1
        inp = Interpreter([])
        str = ""
        while True:
            str += "\n" + input(f"#|BetterKawa:{linenum}|# ")
            linenum += 1
            if (str.count("(") == str.count(")")):
                tokens = Tokenizer(str).get_tokens()
                inp.tokens = tokens
                inp.token_index = 0
                inp.interpret_body(True)
                str = ""
            