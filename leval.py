#file --leval--
# Jakub Grobelny
# 2018

import types
import sys
from pair import pair
from parser import parse
from parser import preparse

#####################
#   EVAL FUNCTION   #
#####################

# list of special forms used to check whether an use of 'define' is legal
notValue = "__!@not_a_value@!__"
specialForms = ["define", "if", "cond", "and", "or", "lambda", "let*", "let", "quote"]
specialValues = ["None", "False", "True"]
basic = [int, float, pair, bool]

# evaluates given expression in given environment
def lispEval(expr, env):

    # since every element in a list is a string at the beginning
    # we need to check if it's convertable to a certain type
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

    def isString(str):
        try:
            if str[0] == str[-1] == '"':
                return True
            return False
        except:
            return False

    # if the expression is not a list
    if not isinstance(expr, list):
        if not expr in env:
            # basic types
            if type(expr) in basic:
                return expr
            if expr in specialForms:
                raise Exception("Invalid use of '" + expr + "'!")
            # boolean types
            if expr == "false" or expr == "False":
                return False
            if expr == "true" or expr == "True":
                return True
            # no value is "__!@not_a_value@!__"
            if expr == "null" or expr == "None" or expr == None:
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
            #TODO:
            # Fix defines inside of another defines
            # Fix defines inside of lambdas
            #if len(expr) == 3:
            if isFloat(expr[1]) or isInt(expr[1]) or isString(expr[1]) or expr[1] in specialValues:
                raise Exception("Can not define a value!")
            elif expr[1] in specialForms:
                raise Exception("Can not define a keyword!")
            else:
                # Syntactic sugar for lambda definitions
                if isinstance(expr[1], list):
                    name = expr[1][0]
                    parameters = expr[1][1:]
                    env.update({name : lispEval(["lambda", parameters, expr[2]], env)})
                else:
                    env.update({expr[1] : lispEval(expr[2], env)})
                return notValue
            #else:
            #    raise Exception("Invalid use of 'define'!")

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

        elif expr[0] == "lambda":
            if len(expr) == 3:
                if not isinstance(expr[1], list):
                    raise ("Invalid use of 'lambda!")
                else:
                    newEnv = {}
                    for symbol in expr[1]:
                        newEnv.update({symbol : None})

                    arity = len(newEnv)
                    body = expr[2]

                    def proc(args, env):
                        locEnv = dict(env)
                        if arity != len(args):
                            raise Exception("Arity mismatch! Expected " + str(arity) + " got " + str(len(args)))
                        for key, arg in zip(newEnv.keys(), args):
                            locEnv[key] = lispEval(arg, env)

                        return lispEval(body, locEnv)

                    return proc 
            else:
                raise Exception("Invalid use of 'lambda'!")
        
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
                            raise Exception("'let' is not recursive! Did you mean 'let*'?")

                lamb = lispEval(["lambda", args, body], env)
                return lamb(argVals, env)

        # recursive let
        #TODO: fix it to make it actually evaluate everything pararelly
        elif expr[0] == "let*":
            if len(expr) != 3:
                raise Exception("Invalid use of 'let*'!")
            else:
                body = expr[2]
                argVals = []
                args = []

                smallEnv = dict(env)

                for definition in expr[1]:
                    if not isinstance(definition, list):
                        raise Exception("Invalid use of 'let*'!")
                    else:
                        args.append(definition[0])
                        argVals.append(definition[1])
                        try:
                            value = lispEval(argVals[-1], smallEnv)
                            smallEnv.update({args[-1] : value})
                        except:
                            smallEnv.update({args[-1] : None})

                for key, val in zip(args, argVals):
                    try:
                        smallEnv.update({key : lispEval(val, smallEnv)})
                    except:
                        raise Exception("Recursive 'let' failed!")
                
                lamb = lispEval(["lambda", args, body], smallEnv)
                return lamb(argVals, smallEnv)

        elif expr[0] == "quote":
            if len(expr) != 2:
                raise Exception("Invalid use of 'quote'")
            else:
                return expr[1]

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
