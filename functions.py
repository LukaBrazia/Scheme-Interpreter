

class Function:
    def __init__(self, func):
        self.func = func
    def execute(self, params):
        return self.func(params)
        
def sub(args):
    if (len(args) == 0):
        print("call to '-' has too few arguments (0; min=1)")
        exit()
    elif (len(args) == 1):
        return -args[0]
    else:
        return args[0] - sum(args[1:])

def mult(args):
    ret = 1
    for arg in args:
        ret *= arg
    return ret

def div(args):
    if (len(args) == 0):
        print("call to '/' has too few arguments (0; min=1)")
        exit()
    elif (len(args) == 1):
        return 1 / args[0]
    else:
        return args[0] / mult(args[1:])

def andexp(args):
    if (len(args) == 0):
        return True
    return args[0] and andexp(args[1:])

def orexp(args):
    if (len(args) == 0):
        return False
    return args[0] or andexp(args[1:])

def car(args):
    if len(args) != 1:
        print("Incorrect number of arguements in call to car")
        exit()
    if not isinstance(args[0], list):
        print("Arguement in call to car must be a list")
        exit()
    if args[0] == []:
        print("Can't call car on an empty list")
        exit()
    return args[0][0]

def cdr(args):
    if len(args) != 1:
        print("Incorrect number of arguements in call to cdr")
        exit()
    if not isinstance(args[0], list):
        print("Arguement in call to cdr must be a list")
        exit()
    if args[0] == []:
        print("Can't call cdr on an empty list")
        exit()
    return args[0][1:]

def cons(args):
    if len(args) != 2:
        print("Incorrect number of arguements in call to cons")
        exit()
    if not isinstance(args[1], list):
        print("Arguement in call to cons must be a list")
        exit()
    return [args[0]] + args[1]

def append(args):
    ret = []
    for l in args:
        ret += l
    return ret

def mapexp(args):
    if len(args) < 2:
        print("Incorrect number of arguements in call to map")
        exit()
    if not isinstance(args[0], Function):
        print("Arguement in call to map not a function")
        exit()
    return [args[0].execute(list(t)) for t in list(zip(*args[1:]))]

def apply(args):
    if len(args) != 2:
        print("Incorrect number of arguements in call to apply")
        exit()
    if not isinstance(args[0], Function):
        print("Arguement in call to apply not a function")
        exit()
    if not isinstance(args[1], list):
        print("Argument in call to apply has to be a list")
        exit()
    return args[0].execute(args[1])

def eval(args):
    if (len(args) != 1):
        print("Incorrect number of arguments in call to eval")
        exit()
    if not isinstance(args[0], list):
        print ("Argumnet to eval must be a list")
        exit()
    if not isinstance(args[0][0], Function):
        print("Argument list to eval must start with a callable object")
        exit()
    return args[0][0].execute(args[0][1:])