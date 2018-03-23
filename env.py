#file --env--
# Jakub Grobelny
# 2018

import sys
from leval import lispEval
from leval import notValue
from leval import isConstant
from leval import isFloat, isInt
from pair import pair
from random import randint
from parser import parse
from parser import preparse
import types

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
    return notValue

def cons(args, env):
    if len(args) != 2:
        raise Exception("cons: arity mismatch!")
    else:
        return pair(lispEval(args[0], env), lispEval(args[1], env))

def car(args, env):
    if len(args) != 1:
        raise Exception("car: arity mismatch!")
    p = lispEval(args[0], env)
    if type(p) != pair:
        raise Exception("car: expected pair, got " + type(p).__name__)
    else:
        return lispEval(p.get(0), env)

def cdr(args, env):
    if len(args) != 1:
        raise Exception("cdr: arity mismatch!")
    p = lispEval(args[0], env)
    if type(p) != pair:
        raise Exception("cdr: expected pair, got " + type(p).__name__)
    else:
        return lispEval(p.get(1), env)

#TODO: change name
def makeList(args, env):
    if len(args) == 0:
        return None
    else:
        return cons([args[0], makeList(args[1:], env)], env)

def isPair(args, env):
    if len(args) != 1:
        raise Exception("pair?: arity mismatch!")
    else:
        if type(lispEval(args[0], env)) == pair:
            return True
        else:
            return False

def isList(args, env):
    if len(args) != 1:
        raise Exception("list?: arity mismatch!")
    else:
        if type(lispEval(args[0], env)) == pair:
            next = cdr([lispEval(args[0], env)], env)
            return isList([next], env)
        else:
            if lispEval(args[0], env) == None:
                return True
            return False

def rand(args, env):
    if len(args) != 2:
        raise Exception("random: arity mismatch!")
    return randint(lispEval(args[0], env), lispEval(args[1], env))

def expt(args, env):
    if len(args) != 2:
        raise Exception("exp: arity mismatch!")
    return lispEval(args[0], env)**lispEval(args[1], env)

def resetEnv(args, env):
    if len(args):
        raise Exception("!reset-env: arity mismatch!")
    else:
        env.clear()
        env.update(globalEnvInit())
    return notValue

def evaluate(args, env):
    if len(args) != 1:
        raise Exception("eval: arity mismatch!")
    else:
        arg = lispEval(args[0], env)

        if isConstant(arg):
            return arg
        # this method is cancerous but it works
        try:
            return lispEval(arg, env)
        except:
            return lispEval(parse(preparse(arg)), env)        

def clear(args, env):
    if len(args):
        raise Exception("!clear: arity mismatch!")
    else:
        print("\n" * 100)
        return notValue

def isNumber(args, env):
    if len(args) != 1:
        raise Exception("number?: arity mismatch!")
    else:
        arg = lispEval(args[0], env)
        return isInt(arg) or isFloat(arg) or (type(arg) in [float, int])

def globalEnvInit():
    # build in definitions
    return {"+" : plus,     
            "-" : minus,    
            "*" : mult,     
            "/" : div,      
            "=" : equal,    
            ">" : greater,  
            "modulo" : mod, 
            "cons" : cons,  
            "car" : car,    
            "cdr" : cdr,    
            "list" : makeList,  
            "list?" : isList,
            "pair?" : isPair,
            "number?" : isNumber,
            "random" : rand,
            "expt" : expt,
            # procedures with '!' as prefix shouldn't really be used
            # (except !exit)
            "!exit" : exit,  
            "!reset-env" : resetEnv,
            "!clear" : clear,
            # eval
            "eval" : evaluate
                            }
