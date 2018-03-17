#file --parser--
# Jakub Grobelny
# 2018

import re

##############
#   PARSER   #
##############

# deleting useless whitespace characters and comments
def preparse(str):

    # removing comments
    str = re.sub(r'\;.+\n', '', str)

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
        if " " in str and str[0] != '"' != str[-1]:
            raise Exception("Incorrect input!")
        else: 
            return str
    else:
        str = str[1:-1]
        result = []

        nested = False
        nestCount = 0
        tempstr = ""
        readingStr = False

        #TODO:
        # 1. do quotations
        # 2. use any type of brackets

        for c in str:

            if (c != ' '):

                tempstr += c
                if c == '"':
                    
                    if not readingStr:
                        readingStr = True
                        
                    else:
                        readingStr = False
                        result.append(tempstr)
                        tempstr = ""

                elif c == '(':
                    nested = True
                    nestCount += 1

                elif c == ')':
                    nestCount -= 1
                    if nestCount == 0:
                        result.append(parse(tempstr))
                        tempstr = ""
                        nested = False

            elif not nested and not readingStr:
                if tempstr != "":
                    result.append(tempstr)
                    tempstr = ""

            elif nested or readingStr:
                tempstr += ' '

        if tempstr != "":
            result.append(tempstr)
        
        return result