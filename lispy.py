# Jakub Grobelny
# 2018
# Something like LISP
# probably

import env
from env import globalEnvInit, lispEval
from parser import parse, preparse
import sys

#############
#    MAIN    #
##############

def interpreter_loop():

    # dictionary used to represent global environment
    globalEnv = globalEnvInit()

    # loading parts of the language written in the language itself (a.k.a. standard library)
    try:
        with open("stdlib.lp", 'r') as stdlibFile:
            stdlib = stdlibFile.read()
            stdlib = parse("(" + preparse(stdlib) + ")")
            for procedure in stdlib:
                try:
                    lispEval(procedure, globalEnv)
                except:
                    raise Exception("Failed to load a definition from stdlib!")
    except:
        print("Failed to open standard library file!\n Make sure stdlib.lp is in the same folder as the interpreter!")

    # interpreting files passed as command line arguments
    if len(sys.argv):
        try:
            for arg in sys.argv[1:]:
                with open(arg, 'r') as file:
                    program = file.read()
                    program = preparse(program)
                    program = "(" + program + ")"
                    expressions = parse(program)

                    for expr in expressions:
                        try:
                            val = lispEval(expr, globalEnv)
                            if val != None:
                                print(val)
                        except Exception as exc:
                            print(exc)

        except:
            print("Failed to open " + sys.argv[1])

    # read-eval-print loop
    while not env.end:
        userInput = input("> ")
        try:
            val = lispEval(parse(preparse(userInput)), globalEnv)
            if val != None:
                print(val)
        except Exception as exc:
            print(exc)

interpreter_loop()