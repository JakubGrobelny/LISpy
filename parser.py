#file --parser.py--

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

        #TODO:
        # 1. do quotations
        # 2. use any type of brackets
        # 3. strings break at spaces

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