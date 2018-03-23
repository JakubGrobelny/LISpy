#file --leval--
# Jakub Grobelny
# 2018

import types
import sys
from pair import pair
from parser import parse
from parser import preparse
from parser import reparse

#####################
#   EVAL FUNCTION   #
#####################

# list of special forms used to check whether an use of 'define' is legal
notValue = "__!@not_a_value@!__"
funcDefinitionsFlag = "__!@contains_definitions@!__"
specialForms = ["define", "if", "cond", "and", "or", "lambda", "let", "quote", "λ"]
specialValues = ["None", "False", "True"]
basic = [int, float, pair, bool]

def isInt(str):
    try:
        int(str)
        return True
    except:
        return False

def isFloat(str):
    try:
        float(str)
        return True
    except:
        return False

def isBool(str):
    return str == "False" or str == "True" or str == False or str == True

def isConstant(arg):
    return isInt(arg) or isFloat(arg) or (type(arg) in basic) or isBool(arg) or (arg == None) or (arg == "None") or isinstance(arg, types.FunctionType)

# evaluates given expression in given environment
def lispEval(expr, env):

    # since every element in a list is a string at the beginning
    # we need to check if it's convertable to a certain type
    
    # if the expression is not a list
    if not isinstance(expr, list):
        if not expr in env:
            # basic types
            if type(expr) in basic:
                return expr
            elif expr in specialForms:
                raise Exception("Invalid use of '" + expr + "'!")
            # boolean types
            elif expr == "False":
                return False
            elif expr == "True":
                return True
            # no value is "__!@not_a_value@!__"
            elif expr == "None" or expr == None:
                return None
            # int (but still represented by string)
            elif isInt(expr):
                return int(expr)
            # float (same as above)
            elif isFloat(expr):
                return float(expr)
            else:
                raise Exception(expr + " is undefined!")
        else:
            return env[expr]

    # else if the expression is a list
    else:
        # checking for special forms first
        if expr[0] == "define":
            if isFloat(expr[1]) or isInt(expr[1]) or expr[1] in specialValues:
                raise Exception("Can not define a value!")
            elif expr[1] in specialForms:
                raise Exception("Can not define a keyword!")
            else:
                # Syntactic sugar for lambda definitions
                if isinstance(expr[1], list):
                    name = expr[1][0]
                    parameters = expr[1][1:]
                    body = expr[2:]
                    body.append({"tag" : None})
                    env.update({name : lispEval(["lambda", parameters, body], env)})
                else:
                    env.update({expr[1] : lispEval(expr[2], env)})
                return notValue

        elif expr[0] == "lambda" or expr[0] == "λ":
            if not isinstance(expr[1], list) or len(expr) < 3:
                raise Exception("Invalid use of 'lambda'!")
            else:
                
                # compressing definitions and stuff into one list to
                # match the way it was done in 'define'

                if len(expr) > 3:
                    exprList = []
                    for expression in expr[2:]:
                        exprList.append(expression)
                else:
                    exprList = [expr[2]]
                    if isinstance(expr[2], list):    
                        if isinstance(expr[2][-1], dict):
                            exprList = expr[2][:-1]

                body = exprList[-1]
                definitions = exprList[:-1]

                newEnv = {}
                for symbol in expr[1]:
                    newEnv.update({symbol : None})

                arity = len(newEnv)                

                def proc(args, env):
                    locEnv = dict(env)
                    if arity != len(args):
                        raise Exception("Arity mismatch! Expected " + str(arity) + " got " + str(len(args)))
                    for key, arg in zip(newEnv.keys(), args):
                        locEnv[key] = lispEval(arg, env)

                    for definition in definitions:
                        lispEval(definition, locEnv)

                    return lispEval(body, locEnv)

                return proc 
        
        elif expr[0] == "let":
            if len(expr) != 3:
                raise Exception("Invalid use of 'let'!")
            else:
                body = expr[2]

                argVals = []
                args = []

                for definition in expr[1]:
                    if not isinstance(definition, list):
                        raise Exception("Invalid use of 'let'!")
                    else:
                        args.append(definition[0])
                        argVals.append(definition[1])
                        
                        try:
                            lispEval(argVals[-1], env)
                        except:
                            raise Exception("Unbound identifier in 'let'!")

                lamb = lispEval(["lambda", args, body], env)
                return lamb(argVals, env)

        elif expr[0] == "quote":
            if len(expr) != 2:
                raise Exception("Invalid use of 'quote'")
            else:
                if isConstant(expr[1]):
                    return lispEval(expr[1], env)
                else:
                    return reparse(expr[1])

        elif expr[0] == "if":
            if len(expr) != 4:
                raise Exception("Invalid use of 'if'!")
            else:
                if not lispEval(expr[1], env):
                    return lispEval(expr[3], env)
                else:
                    return lispEval(expr[2], env)

        elif expr[0] == "cond":
            for cond in expr[1:]:
                if len(cond) != 2:
                    raise Exception("Invalid use of 'cond'!")
                else:
                    if lispEval(cond[0], env):
                        return lispEval(cond[1], env)

        elif expr[0] == "and":
            for pred in expr[1:]:
                if not lispEval(pred, env):
                    return False
            return True

        elif expr[0] == "or":
            for pred in expr[1:]:
                if lispEval(pred, env):
                    return True
            return False

        # calculating operator
        elif type(expr[0]) == list:
            op = lispEval(expr[0], env)

            try:
                args = expr[1:]
            except:
                args = []

            try:
                return op(args, env)
            except:
                raise Exception(op.__name__ + ": arity mismatch!")

        # searching for operator in the environment
        elif expr[0] in env:
            if isinstance(env[expr[0]], types.FunctionType):
                return lispEval(expr[0], env)(expr[1:], env)

        # expression was invalid
        else:
            raise Exception('(' + ' '.join(expr) + ')' + " is not a valid expression!")
