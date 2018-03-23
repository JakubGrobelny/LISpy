#file --writer--
# Jakub Grobelny
# 2018

from env import car, cdr
from pair import pair
import types

# function that prints values in certain formats
def present(value):
    
    #TODO: print lists recursively
    if type(value) == pair:
        ls = [value.get(0)]
        realLength = 0
        while type(value) == pair:
            realLength += 1
            value = value.get(1)
            if type(value) == pair:
                ls.append(value.get(0))
        if value != None:
            ls.append(value)
        
        if realLength == 1:
            print("(" + str(ls[0]) + " . " + str(ls[1]) + ")")
        else:
            print("(" + ' '.join(map(str, ls)) + ")")
    
    elif isinstance(value, types.FunctionType):
        print("#<procedure:" + value.__name__ + ">")
    elif value != "__!@not_a_value@!__":
        print(value)    
