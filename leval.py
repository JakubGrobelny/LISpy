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
specialForms = ["define", "if", "cond", "and", "or", "lambda"]

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

    basic = {int, float, pair}

    # if the expression is not a list
    if not isinstance(expr, list):
        if not expr in env:
            # basic types
            if type(expr) in basic:
                return expr
            # boolean types
            if expr == "false" or expr == "#f":
                return False
            if expr == "true" or expr == "#t":
                return True
            if expr == "null":
                return "null"
            # quotes (and characters)
            if expr[0] == '\'':
                return expr
            # symbols are strings so we return string
            if expr[0] == expr[-1] == '\"':
                return expr
            # int (but still represented by string)
            elif isInt(expr):
                return int(expr)
            # float (same as above)
            elif isFloat(expr):
                return float(expr)
            else:
                raise Exception(expr + " is of unknown type!")
        else:
            return env[expr]
    # else if the expression is a list
    else:

        # checking for special forms first
        if expr[0] == "define":
            #TODO:
            # Fix defines inside of another defines
            if len(expr) == 3:
                if isFloat(expr[1]) or isInt(expr[1]) or isString(expr[1]):
                    raise Exception("Can not define a value!")
                elif expr[1] in specialForms:
                    raise Exception("Can not define a keyword!")
                else:
                    env.update({expr[1] : lispEval(expr[2], env)})
            else:
                raise Exception("Invalid use of 'define'!")

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

        #TODO: elif expr[0] == "lambda":
        # lambdas will need own local environments

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
