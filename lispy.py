# Jakub Grobelny
# 2018
# Something like LISP
# probably

import env
from env import globalEnvInit, lispEval, notValue
from parser import parse, preparse
from writer import present
import sys
#import resource
#import threading

##############
#    MAIN    #
##############

def printInfo():
    print("LISpy version 0.1")
    print("Type \"(!exit)\" to exit")

def interpreterLoop():

    # dictionary used to represent global environment
    globalEnv = globalEnvInit()
    sys.setrecursionlimit(10000)
    #resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
    #threading.stack_size(10**9)

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
                                present(val)
                        except Exception as exc:
                            print(exc)

        except:
            print("Failed to open " + sys.argv[1])

    printInfo()

    # read-eval-print loop
    while not env.end:
        userInput = input(">>> ")
        try:
            val = lispEval(parse(preparse(userInput)), globalEnv)
            present(val)
        except Exception as exc:
            print(exc)

interpreterLoop()