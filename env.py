#file --env--

import sys
from leval import lispEval

# global variable used to determine whether the program should close
end = False

####################
# Basic procedures #
####################
#TODO: expand them to work with strings and stuff

def plus(args, env):

    sum = 0
    for arg in args:
        sum += lispEval(arg, env)
    return sum

def minus(args, env):

    if len(args) == 1:
            return -lispEval(args[0], env)
    elif len(args) > 0:
        sum = lispEval(args[0], env)
    else:
        raise Exception("-: arity mismatch!")

    for arg in args[1:]:
        sum -= lispEval(arg, env)

    return sum

def mult(args, env):

    prod = 1
    for arg in args:
        prod *= lispEval(arg, env)
    return prod

def div(args, env):

    if len(args) == 1:
        return 1 / lispEval(args[0], env)
    elif len(args) > 0:
        quot = lispEval(args[0], env)
    else:
        raise Exception("/: arity mismatch!")

    for arg in args[1:]:
        quot /= lispEval(arg, env)

    return quot

def equal(args, env):

    if not args:
        raise Exception("=: arity mismatch!")
    prev = lispEval(args[0], env)

    for arg in args[1:]:
        if (lispEval(arg, env) != prev):
            return False
        prev = lispEval(arg, env)

    return True

def greater(args, env):

    if len(args) < 2:
        raise Exception(">: arity mismatch!")
    
    first = lispEval(args[0], env)

    for arg in args[1:]:
        if (lispEval(arg, env) >= first):
            return False
    return True

def mod(args, env):
  
    if len(args) != 2:
        raise Exception("modulo: arity mismatch!")
    
    return lispEval(args[0], env) % lispEval(args[1], env)
    
def exit(args, env):
    global end
    end = True

def globalEnvInit():

    # build in definitions
    return {"+" : plus,     \
            "-" : minus,    \
            "*" : mult,     \
            "/" : div,      \
            "=" : equal,    \
            ">" : greater,  \
            "modulo" : mod, \
            "exit" : exit
                            }
