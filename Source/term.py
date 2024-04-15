
# term type
CONST_ATOM = "Atom"
CONST_NUMBER = "Number"
CONST_VARIABLE = "Variable"
CONST_COMPLEX = "ComplexTerm"


def splitWithParenLevel(inp:str, start:int, end:int, delim:str, indexList = []):
    parenCount = 0
    startStr = start
    strList = []
    for index in range(start, end + 1):
        if inp[index] == '(':
            parenCount += 1
        elif inp[index] == ')':
            parenCount -= 1
        elif parenCount == 0:
            if (inp[index: (index + len(delim))] == delim):
                strList.append(inp[startStr:index])
                indexList.append([startStr, (index - 1)])
                startStr = index + 1 + len(delim)
                index += 1
        if parenCount == 0 and index == end:
            strList.append(inp[startStr:(index + 1)])
            indexList.append([startStr, index])
            break
    return strList

def isAtom(inp:str):
    if inp[0] == '\'' and inp[-1] == '\'':
        return True
    else:
        case1 = (inp[0].islower())
        case3 = not case1
        for c in inp:
            if c.isalnum() or c == '_':
                if case3:
                    return False
            else:
                if case1:
                    return False
        return case1 or case3
   
def isNumber(inp:str):
    try:
        n = int(inp)
        return True
    except ValueError:
        return False
        
def isVar(inp:str):
    for c in inp:
        if (not c.isalnum()) and c != '_':
            return False
    return (inp[0].isupper() or inp[0] == '_')

class Term:
    def __init__(self, inp:str = ""):
        self.type = None
        self.ss = ""
        self.functor = ""
        self.arguments = []
        if len(inp) == 0:
            return
        if isAtom(inp):
            self.type = CONST_ATOM
        elif isNumber(inp):
            self.type = CONST_NUMBER
        elif isVar(inp):
            self.type = CONST_VARIABLE
        else:
            # find open and close parentheses
            openPare = inp.find('(')
            if openPare == -1 or inp[-1] != ')':
                return
            
            # check if it is a expresision
            level = 0
            for ind in range(len(inp) - 1):
                if inp[ind] == '(':
                    level += 1
                elif inp[ind] == ')':
                    level -= 1
                if level == 0 and (inp[ind] == ';' or inp[ind] == ',' or inp[ind:(ind + 2)] == ':-'):
                    return
                
            # get functor
            self.functor = inp[:openPare]
            if (not isAtom(self.functor)):
                return
            
            # split to create arguments by ', '
            termList = splitWithParenLevel(inp, openPare + 1, len(inp) - 2, ',')
            for term in termList:
                tem = Term(term)
                if tem.type:
                    self.arguments.append(tem)
            
            # set type
            self.type = CONST_COMPLEX
            
        if (self.type):
            self.ss = inp
    
    def updateStr(self):
        if self.type != CONST_COMPLEX:
            return self.ss
        else:
            indexList = []
            argList = splitWithParenLevel(self.ss, len(self.functor) + 1, len(self.ss) - 2, ',', indexList)
            for ind, arg in enumerate(argList):
                newArg = self.arguments[ind].updateStr()
                lenDiff = len(arg) - len(newArg)
                self.ss = self.ss.replace(arg, newArg)
                if (lenDiff != 0):
                    # update the after indexes
                    for i in range(ind + 1, len(indexList)):
                        indexList[i][0] += lenDiff
                        indexList[i][1] += lenDiff
            return self.ss
    
    def getSubType(self, varList:list = [], typee = CONST_VARIABLE):
        if (self.type == None):
            varList = []
            return False
        elif (self.type == typee):
            appeared = False
            for var in varList:
                if (self.ss == var):
                    appeared = True
                    break
            if not appeared:
                varList.append(self.ss)
            return True
        elif (self.type == CONST_COMPLEX):
            return all(arg.getSubType(varList, typee) for arg in self.arguments)
        else:
            return True
    
    def assignValueToVariable(self, var, val):
        if (self.type == CONST_VARIABLE and self.ss == var.ss):
            self.ss = val.ss
            return Term(val.ss)
        elif (self.type == CONST_COMPLEX):
            for index, arg in enumerate(self.arguments):
                newarg = arg.assignValueToVariable(var, val)
                if (newarg != None):
                    self.arguments[index] = newarg
                    self.arguments[index].ss = newarg.ss
            return self
        else:
            return None
        


                    
def occur_check(var, x, sub):
    if var.ss == x.ss:
        return True
    elif x.type == CONST_VARIABLE and x in sub:
        return occur_check(var, sub[x], sub)
    elif x.type == CONST_COMPLEX:
        return any(occur_check(var, xi, sub) for xi in x.arguments)
    else:
        return False

def unify_var(var, x, sub):
    for k in sub.keys():
        if var.ss == k.ss:
            return unify(sub[k], x, sub)
        elif x.ss == k.ss:
            return unify(var, sub[k], sub)
    if occur_check(var, x, sub):
        sub = None
        return None
    else:
        # replace x
        # example: {X/abc, Y/sth(X)} -> {X/abc, Y/sth(abc)}
        sth = Term(x.ss)
        for key, val in sub.items():
            sth.assignValueToVariable(key, val)
        sth.ss = sth.updateStr()
        sub[var] = sth
        return sub

def unify(x, y, sub = {}):
    if sub == None: # failure
        return None
    if x == y:
        return sub
    elif isinstance(x, Term) and isinstance(y, Term):
        if x.ss == y.ss:
            return sub
        elif x.type == CONST_VARIABLE:
            return unify_var(x, y, sub)
        elif y.type == CONST_VARIABLE:
            return unify_var(y, x, sub)
        elif x.type == CONST_COMPLEX and y.type == CONST_COMPLEX\
            and x.functor == y.functor and len(x.arguments) == len(y.arguments):
            return unify(x.arguments, y.arguments, unify(x.functor, y.functor, sub))
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        extractX = x[0]
        extractY = y[0]
        x.pop(0)
        y.pop(0)
        return unify(x, y, unify(extractX, extractY, sub))
    else:
        sub = None
        return None

def safe_unify(termX:Term, termY:Term, sub = {}):
    if (termX.ss == termY.ss):
        return sub, termX, termY
    tempX = Term(termX.ss)
    tempY = Term(termY.ss)
    if unify(termX, termY, sub):
        # after unify, 2 terms become empty so I return it back to its original form
        return sub, tempX, tempY
    else:
        return None, tempX, tempY

def substitute(sub, term:Term):
    if sub == None or len(sub) == 0:
        return term
    else:
        # get variable lists
        varList = []
        if not term.getSubType(varList):
            return term

        # assign value to each variable
        tempTerm = Term(term.ss)
        for key, val in sub.items():
            if key.ss in varList:
                tempTerm.assignValueToVariable(key, val)
        tempTerm.ss = tempTerm.updateStr()
        return tempTerm
