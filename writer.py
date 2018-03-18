#file --writer--
# Jakub Grobelny
# 2018

from env import car, cdr
from pair import pair

# function that prints values in certain formats
def present(value):
    
    if type(value) == pair:
        ls = [value.get(0)]
        while type(value) == pair:
            value = value.get(1)
            if type(value) == pair:
                ls.append(value.get(0))
        if value != "null":
            ls.append(value)
        print("'(" + ' '.join(map(str, ls)) + ")")
    else:
        print(value)    
    