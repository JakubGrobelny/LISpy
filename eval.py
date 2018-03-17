# Jakub Grobelny
# 2018
# Something like LISP
# probably

import types

# deleting useless whitespace characters
def preparse(str):

    str = str.replace('\n', " ")
    str = str.replace('\t', " ")
    str = str.replace('\v', " ")
    str = str.replace('\f', " ")
    str = str.replace('\r', " ")

    while "  " in str:
        str = str.replace("  ", " ")

    return str

# parses s-expressions into lists
def parse(str):

    if "(" not in str and ")" not in str:
        if " " in str:
            raise Exception("Incorrect input!")
        else: 
            return str
    else:
        str = str[1:-1]
        result = []

        nested = False
        nestCount = 0
        tempstr = ""

        for c in str:
            if (c != ' '):
                tempstr += c
                if c == '(':
                    nested = True
                    nestCount += 1
                elif c == ')':
                    nestCount -= 1
                    if nestCount == 0:
                        result.append(parse(tempstr))
                        tempstr = ""
                        nested = False
            elif not nested:
                if tempstr != "":
                    result.append(tempstr)
                    tempstr = ""
            elif nested:
                tempstr += ' '

    if tempstr != "":
        result.append(tempstr)
        
    return result

# evaluates given expression in given environment
def lispEval(expr, env):

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

    if not isinstance(expr, list):
        if not expr in env:
            # quotes (and characters)
            if expr[0] == '\'':
                return expr
            # symbols are strings so we return string
            if expr[0] == expr[-1] == '\"':
                return expr
            elif isInt(expr):
                return int(expr)
            elif isFloat(expr):
                return float(expr)
            else:
                raise Exception(expr + " is of unknowny type!")
        else:
            return env[expr]
    else:
        if expr[0] == "define":
            if len(expr) == 3:
                env.update({expr[1] : lispEval(expr[2], env)})
            else:
                raise Exception("Invalid use of 'define'")
        elif expr[0] in env:
            if isinstance(env[expr[0]], types.FunctionType):
                return env[expr[0]](expr[1:], env)
        else:
            raise Exception('(' + ' '.join(expr) + ')' + " is not a valid expression!")
        
def interpreter_loop():
    exit = False
    globalEnv = {"+" : plus}
    #TODO: load and eval a file before entering interpreter loop
    while not exit:
        userInput = input()
        if userInput == "#exit":
            exit = True
        else:
            #print(parse(preparse(userInput)))
            val = (lispEval(parse(preparse(userInput)), globalEnv))
            if val:
                print(val)

# Basic procedures:

def plus(args, env):
    sum = 0
    for arg in args:
        sum += lispEval(arg, env)
    return sum

interpreter_loop()