# Jakub Grobelny
# 2018
# Something like LISP
# probably

import types

# parses user input into symbol list
def parse(str):
    out = []
    if "(" not in str and ")" not in str:
        if " " in str:
            raise Exception("Incorrect input!")
        else: 
            return str
    else:
        str = str[1:-1]
        tempstr = ""
        result = []
        nested = False
        nestCount = 0
        for c in str:
            if (c != " "):  
                tempstr += c
                if c == "(":
                    nested = True
                    nestCount += 1
                elif c == ")":
                    nestCount -= 1
                    if nestCount == 0:
                        result.append(parse(tempstr))
                        tempstr = ""
                        nested = False
            elif not nested:
                result.append(tempstr)
                tempstr = ""
            elif nested:
                tempstr += " "
    return result

# evaluates given expression in given environment
def eval(expr, env):
    return 0 #TODO:

def interpreter_loop():
    exit = False
    globalEnv = {}
    while not exit:
        userInput = input()
        if userInput == "exit":
            exit = True
        else:
            print(parse(userInput))
            #eval(parse(userInput), globalEnv)

interpreter_loop()