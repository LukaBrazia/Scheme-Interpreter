class Function:
    def __init__(self, func):
        self.func = func
    def execute(self, params):
        return self.func(self)
        
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