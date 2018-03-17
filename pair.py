#file --pair--
# Jakub Grobelny
# 2018

class pair:
    
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def get(self, which):
        if which == 0:
            return self.first
        elif which == 1:
            return self.second
        else:
            raise Exception("Pair access violation!")