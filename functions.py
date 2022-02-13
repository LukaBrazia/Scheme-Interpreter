
import math

class Function:
    def __init__(self, func):
        self.func = func
    def execute(self, params):
        return self.func(params)
        
def newline(args):
    print()

def sub(args):
    if (len(args) == 0):
        print("call to '-' has too few arguments (0 min=1)")
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
        print("call to '/' has too few arguments (0 min=1)")
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
        print("Incorrect number of aruments in call to car")
        exit()
    if not isinstance(args[0], list):
        print("arument in call to car must be a list")
        exit()
    if args[0] == []:
        print("Can't call car on an empty list")
        exit()
    return args[0][0]

def cdr(args):
    if len(args) != 1:
        print("Incorrect number of aruments in call to cdr")
        exit()
    if not isinstance(args[0], list):
        print("arument in call to cdr must be a list")
        exit()
    if args[0] == []:
        print("Can't call cdr on an empty list")
        exit()
    return args[0][1:]

def cons(args):
    if len(args) != 2:
        print("Incorrect number of aruments in call to cons")
        exit()
    if not isinstance(args[1], list):
        print(args[1])
        print("arument in call to cons must be a list")
        exit()
    return [args[0]] + args[1]

def append(args):
    ret = []
    for l in args:
        ret += l
    return ret

def mapexp(args):
    if len(args) < 2:
        print("Incorrect number of aruments in call to map")
        exit()
    if not isinstance(args[0], Function):
        print("arument in call to map not a function")
        exit()
    return [args[0].execute(list(t)) for t in list(zip(*args[1:]))]

def apply(args):
    if len(args) != 2:
        print("Incorrect number of aruments in call to apply")
        exit()
    if not isinstance(args[0], Function):
        print("arument in call to apply not a function")
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

def null(args):
    if (len(args) != 1):
        print("Incorrect number of arguments in call to null")
        exit()
    if not isinstance(args[0], list):
        print ("Argumnet to null? must be a list")
    return args[0] == []

def length(args):
    if not isinstance(args[0], list):
        print ("Argumnet to list must be a list")
    return len(args[0])

def display(args):
    if (len(args) != 1):
        print("Incorrect number of arguments in call to display")
        exit()
    print(kawaPrint(args[0]), end="")

def num_eq(args):
    if (len(args) < 2):
        print("Incorrect number of aruments in call to numeric compare")
        exit()
    for tok1, tok2 in zip(args, args[1:]):
        if tok1 != tok2:
            return False
    return True

def num_lt(args):
    if (len(args) < 2):
        print("Incorrect number of aruments in call to numeric compare")
        exit()
    for tok1, tok2 in zip(args, args[1:]):
        if tok1 >= tok2:
            return False
    return True

def num_gt(args):
    if (len(args) < 2):
        print("Incorrect number of aruments in call to numeric compare")
        exit()
    for tok1, tok2 in zip(args, args[1:]):
        if tok1 <= tok2:
            return False
    return True

def num_le(args):
    if (len(args) < 2):
        print("Incorrect number of aruments in call to numeric compare")
        exit()
    for tok1, tok2 in zip(args, args[1:]):
        if tok1 > tok2:
            return False
    return True

def num_ge(args):
    if (len(args) < 2):
        print("Incorrect number of aruments in call to numeric compare")
        exit()
    for tok1, tok2 in zip(args, args[1:]):
        if tok1 < tok2:
            return False
    return True

def equal(args):
    if (len(args) != 2):
        print("Incorrect number of aruments in call to equal?")
        exit()
    return args[0] == args[1]

def zero(args):
    if (len(args) != 1):
        print("Incorrect number of aruments in call to zero?")
        exit()
    return args[0] == 0

def remainder(args):
    if (len(args) != 2):
        print("Incorrect number of aruments in call to remainder")
        exit()
    return args[0] % args[1]

def quotient(args):
    if (len(args) != 2):
        print("Incorrect number of aruments in call to quotient")
        exit()
    return args[0] // args[1]

def ls(args):
    return args

def positive(args):
    if (len(args) != 1):
        print("Incorrect number of aruments in call to positive?")
        exit()
    return args[0] > 0

def negative(args):
    if (len(args) != 1):
        print("Incorrect number of aruments in call to negative?")
        exit()
    return args[0] < 0

def odd(args):
    if (len(args) != 1):
        print("Incorrect number of aruments in call to odd?")
        exit()
    return args[0] % 2 == 1

def even(args):
    if (len(args) != 1):
        print("Incorrect number of aruments in call to even?")
        exit()
    return args[0] % 2 == 0

def expt(args):
    if (len(args) != 2):
        print("Incorrect number of aruments in call to expt")
        exit()
    return args[0] ** args[1]

def sqrt(args):
    if (len(args) != 1):
        print("Incorrect number of aruments in call to sqrt")
        exit()
    return math.sqrt(args[0])

def kawaPrint(args):
    st = ""
    if isinstance(args, list):
        st += "("
        for arg in args:
            st += kawaPrint(arg) + " "
        st = st[:-1]
        st += ")"
    elif isinstance(args, bool):
        if args:
            st += "#t"
        else:
            st += "#f"
    else:
        st += str(args)
    return st

def reverse(args):
    if len(args) != 1:
        print("Incorrect number of aruments in call to reverse")
        exit()
    if not isinstance(args[0], list):
        print("Argument in call to reverse must be a list")
        exit()
    l2 = args[0].copy()
    l2.reverse()
    return l2