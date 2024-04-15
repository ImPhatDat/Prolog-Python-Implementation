from term import *
import random
# expression type
CONST_FACT = "Fact"
CONST_RULE = "Rule"

import itertools
def printSubstitute(sub:dict):
    if (len(sub) == 0):
        return
    sub = dict(sorted(sub.items(), key=lambda x: x[0].ss))
    first = True
    for key, val in sub.items():
        if first:
            print(key.ss + " = " + val.ss, end="")
            first = False
        else:
            print(", " + key.ss + " = " + val.ss, end="")
    print(".")

def differentSub(sub1:dict, sub2:dict, varSet:set):
    for v in varSet:
        val1 = None
        for key, value in sub1.items():
            if v == key.ss:
                val1 = value
                break
        for key, value in sub2.items():
            if v == key.ss:
                if val1.ss != value.ss:
                    return True
                else:
                    break
    return False

class Relationship:
    def __init__(self, operator, term1, term2):
        self.operator = operator
        self.term1 = term1
        self.term2 = term2

class Rule:
    def __init__(self, ss, consequent, antecedent):
        self.ss = ss
        self.consequent = consequent
        self.antecedent = antecedent

def mergeAndSubs(subsList: list[list[dict]], varSet: set[str]) -> list[dict]:
    # varSet = ('X', 'Y', 'Z')
    # subsList = [
        # [{Term('X'): Term('a'), Term('Y'): Term('b')}, {Term('X'): Term('c'), Term('Y'): Term('d')}], 
        # [{Term('Y'): Term('b'), Term('Z'): Term('e')}, {Term('Y'): Term('s'), Term('Z'): Term('f')}]
        # ]
    # output: [{Term('X'): Term('a'), Term('Y'): Term('b'), Term('Z'): Term('e')}]
    
    
    res = []
    varSet = list(varSet)
    intersecct = [[] for _ in range(len(varSet))]
    
    if len(subsList) == 1 or len(varSet) == 1:
        for s in subsList:
            for sub in s:
                notin = True
                for r in res:
                    if not differentSub(r, sub, varSet):
                        notin = False
                        break
                if notin:
                    res.append(sub)
        return res
    
    # for ss in subsList:
    #     print("------------------")
    #     for sub in ss:
    #         printSubstitute(sub)
    
    # find intersection of variable positions
    for id, subs in enumerate(subsList):
        if len(subs) != 0:
            for k, v in subs[0].items():
                try:
                    intersecct[varSet.index(k.ss)].append(id)
                except ValueError:
                    pass
    
    specialCase = True
    for id in range(len(varSet)):
        if len(intersecct[id]) != 1:
            specialCase = False
            break
        
    if specialCase:
        for pair in itertools.product(*subsList):
            if len(pair) != len(varSet):
                continue
            sub = {}
            for su in pair:
                sub.update(su)
            exist = False
            for r in res:
                if not differentSub(r, sub, varSet):
                    exist = True
                    break
            if not exist:
                res.append(sub)
    else:
        # merge
        for ind, subs in enumerate(subsList):
            for iddd, sub in enumerate(subs):
                merged = {}
                addSub = []
                allValid = True
                
                for keySub, valSub in sub.items():
                    try:
                        getPos = varSet.index(keySub.ss)
                    except ValueError:
                        continue
                    for io, othSub in enumerate(subsList):
                        if io not in intersecct[getPos]:
                            for os in othSub:
                                addSub.append(os)
                            
                    for section in intersecct[getPos]:
                        if section != ind:
                            found = False
                            for otherSub in subsList[section]:
                                for k, v in otherSub.items():
                                    if k.ss == keySub.ss and v.ss == valSub.ss:
                                        found = True
                                        addSub.append(otherSub)
                            if not found:
                                allValid = False
                                break
                    if not allValid:
                        break 
                if allValid:
                    for ad in addSub:
                        merged = sub.copy()
                        for k, v in ad.items():
                            diff = True
                            for ks in sub.keys():
                                if k.ss == ks.ss:
                                    diff = False
                                    break
                            if diff:
                                merged[Term(k.ss)] = Term(v.ss)
                        if len(merged) == len(varSet):
                            exist = False
                            for r in res:
                                if not differentSub(r, merged, varSet):
                                    exist = True
                                    break
                            if not exist:
                                res.append(merged)
                        merged = sub.copy()
                else:
                    subs.pop(iddd)
    return res    

def findEqual(varSet: set[str], atomList:list[str]) -> list[dict]:
    res = []
    for at in atomList:
        sub = {}
        for v in varSet:
            sub[Term(v)] = Term(at)
        res.append(sub)
    return res

def findDiff(varSet: set[str], atomList:list[str]) -> list[dict]:
    res = []
    for in1 in range(len(atomList)):
        for in2 in range(len(atomList)):
            sub = {}
            first = True
            for v in varSet:
                if first:
                    sub[Term(v)] = Term(atomList[in1])
                    first = False
                else:
                    sub[Term(v)] = Term(atomList[in2])
            res.append(sub)
    return res

def haveSameFunctors(sen1, sen2):
    vars1 = sen1.getVariableSet()
    vars2 = sen2.getVariableSet()
    if len(vars1) != len(vars2):
        return False
    s1 = str(sen1.ss)
    s2 = str(sen2.ss)
    for v in vars1:
        s1 = s1.replace(v, "")
    for v in vars2:
        s2 = s2.replace(v, "")
    
    return s1 == s2

def standardizeVariable(rule, goal, goalVarList):
    if not haveSameFunctors(Expression(rule.consequent.ss), goal):
        return False, rule
    varRule = []
    if not rule.consequent.getSubType(varRule, CONST_VARIABLE):
        return False, rule
    newStr = str(rule.ss)
    for ind, v in enumerate(varRule):
        newStr = newStr.replace(v, goalVarList[ind])
    exp = Expression(newStr)
    return True, exp.contains
    
def getAll(varSet:set[str], atomList:list):
    res = []
    maxSubs = len(atomList) ** len(varSet)
    while True:
        sub = {}
        for v in varSet:
            sub[Term(v)] = Term(random.choice(atomList))
        newS = True
        for r in res:
            if not differentSub(r, sub, varSet):
                newS = False
                break
        if newS:
            res.append(sub)
            if len(res) == maxSubs:
                break
    return res
    
class Expression:
    def __init__(self, inp:str):
        self.relations = list[Relationship]()
        self.contains = None
        self.type = None
        self.ss = inp
        if len(inp) == 0:
            return
        if inp[0] == '(' and inp[-1] == ')':
            inp = inp[1:-1]
        inp = inp.strip()
        
        #split on ':-' to detect rule or fact
        expList = splitWithParenLevel(inp, 0, len(inp) - 1, ' :-')
        if len(expList) == 1: # no ':-' found -> must be a fact
            self.type = CONST_FACT
            expList = splitWithParenLevel(inp, 0, len(inp) - 1, ';')
            if len(expList) != 1: # or
                for i in range(len(expList) - 1):
                    self.relations.append(Relationship(';', 
                                                        Expression(expList[i]), 
                                                        Expression(expList[i + 1])))
            else: # and
                expList = splitWithParenLevel(inp, 0, len(inp) - 1, ',')
                if len(expList) != 1:
                    for i in range(len(expList) - 1):
                        self.relations.append(Relationship(',', 
                                                            Expression(expList[i]), 
                                                            Expression(expList[i + 1])))
                else: # equal
                    expList = splitWithParenLevel(inp, 0, len(inp) - 1, ' =')
                    if len(expList) != 1:
                        for i in range(len(expList) - 1):
                            self.relations.append(Relationship('=', 
                                                            Expression(expList[i]), 
                                                            Expression(expList[i + 1])))
                    else: # different
                        expList = splitWithParenLevel(inp, 0, len(inp) - 1, ' \\=')
                        if len(expList) != 1:
                            for i in range(len(expList) - 1):
                                self.relations.append(Relationship('\\=', 
                                                                Expression(expList[i]), 
                                                                Expression(expList[i + 1])))
                        else: # single term
                            self.contains = Term(inp)
        else: 
            # examine the first expression
            #   check first expression
            tem = Term(expList[0])
            if (tem.type != None): # single
                isRule = True
                for arg in tem.arguments:
                    if arg.type != CONST_VARIABLE:
                        isRule = False
                        break
                if isRule: # is rule
                    self.type = CONST_RULE
                    conse = tem # consequent must be a term
                    ante = [Expression(ar) for ar in splitWithParenLevel(expList[1], 0, len(expList[1]) - 1, ',')]
                    self.contains = Rule(inp, conse, ante)
                else: # is fact
                    self.type = CONST_FACT
                    self.relations.append(Relationship(':-', Expression(expList[0]), Expression(expList[1])))
            else: # not single -> must be a fact
                self.type = CONST_FACT
                self.relations.append(Relationship(':-', Expression(expList[0]), Expression(expList[1])))
    
    def getSubexpList(self):
        if len(self.relations) == 0:
            return self
        expList = []
        for ind in range(0, len(self.relations), 2):
            expList.append(self.relations[ind].term1)
            expList.append(self.relations[ind].term2)
            
        if len(self.relations) % 2 == 0:
            expList.append(self.relations[len(self.relations) - 1].term2)
        return expList

    def getAllAtom(self):
        atoms = set()
        if self.contains != None:
            if self.type == CONST_FACT:
                subAtoms = []
                if not self.contains.getSubType(subAtoms, CONST_ATOM):
                    return set()
                for sub in subAtoms:
                    atoms.add(sub)
        else:
            expList = self.getSubexpList()
            for exp in expList:
                res = exp.getAllAtom()
                for r in res:
                    atoms.add(r)
        return atoms
                
    def updateNewStr(self):
        if self.contains != None:
            if self.type == CONST_FACT:
                self.contains.ss = self.contains.updateStr()
                self.ss = self.contains.ss
            elif self.type == CONST_RULE:
                self.contains.consequent.ss = self.contains.consequent.updateStr()
                st = self.contains.consequent.ss + " :- "
                for ind in range(len(self.contains.antecedent) - 1):
                    self.contains.antecedent[ind].ss = self.contains.antecedent[ind].updateNewStr()
                    st += self.contains.antecedent[ind].ss + ", "
                self.contains.antecedent[len(self.contains.antecedent) - 1].ss = self.contains.antecedent[len(self.contains.antecedent) - 1].updateNewStr()
                st += self.contains.antecedent[len(self.contains.antecedent) - 1].ss
                self.ss = st
        else:
            st = ""
            for ind in range(0, len(self.relations), 2):
                self.relations[ind].term1.ss = self.relations[ind].term1.updateNewStr()
                self.relations[ind].term2.ss = self.relations[ind].term2.updateNewStr()
                
                st += self.relations[ind].term1.ss
                
                if self.relations[ind].operator != "," and self.relations[ind].operator != ";":
                    st += " "
                st += self.relations[ind].operator + " "
                
                st += self.relations[ind].term2.ss
                
                if ind != len(self.relations) - 1:
                    if self.relations[ind].operator != "," and self.relations[ind].operator != ";":
                        st += " "
                    st += self.relations[ind].operator + " "
                    
            if len(self.relations) % 2 == 0:
                self.relations[len(self.relations) - 1].term2.ss = self.relations[len(self.relations) - 1].term2.updateNewStr()
                st += self.relations[len(self.relations) - 1].term2.ss
            self.ss = st
        return self.ss
            
    def getVariableSet(self, typee = CONST_VARIABLE):
        varSet = set()
        if self.contains != None and self.type == CONST_RULE:
            var = []
            self.contains.consequent.getSubType(var, typee)
            for v in var:
                varSet.add(v)
            for ante in self.contains.antecedent:
                res = ante.getVariableSet(typee)
                for r in res:
                    varSet.add(r)
        elif self.contains != None and self.type == CONST_FACT:
            varList = []
            if not self.contains.getSubType(varList, typee):
                pass
            if len(varList) == 0:
                pass
            else:
                for v in varList:
                    varSet.add(v)
        else:
            expList = self.getSubexpList()
            for exp in expList:
                res = exp.getVariableSet(typee)
                for r in res:
                    varSet.add(r)
        return varSet
    
    def getVariableList(self, typee = CONST_VARIABLE):
        varSet = []
        if self.contains != None and self.type == CONST_RULE:
            var = []
            self.contains.consequent.getSubType(var, typee)
            for v in var:
                if v not in varSet:
                    varSet.append(r)
            for ante in self.contains.antecedent:
                res = ante.getVariableList(typee)
                for r in res:
                    if r not in varSet:
                        varSet.append(r)
        elif self.contains != None and self.type == CONST_FACT:
            varList = []
            if not self.contains.getSubType(varList, typee):
                pass
            if len(varList) == 0:
                pass
            else:
                for v in varList:
                    if v not in varSet:
                        varSet.append(v)
        else:
            expList = self.getSubexpList()
            for exp in expList:
                res = exp.getVariableList(typee)
                for r in res:
                    if r not in varSet:
                        varSet.append(r)
        return varSet
        
    def getValue(self, facts:list, rules:list, atomList:list) -> bool: # idea: backward chaining algorithm
        # check facts
        if self.type == CONST_FACT and self.contains != None:
            if self.contains.functor == "not":
                if (not Expression(self.contains.arguments[0].ss).getValue(facts, rules, atomList)):
                    return True
            for fact in facts:
                if fact.contains != None:
                    if fact.ss == self.contains.ss:
                        return True
                    # unify
                    sub = {}
                    res, fact.contains, self.contains = safe_unify(fact.contains, self.contains, sub)
                    if res:
                        return True
                elif fact.relations[0].operator == ':-':
                    if fact.relations[0].term1.ss == self.ss:
                        if fact.relations[0].term2.getValue(facts, rules, atomList):
                            return True
                    elif len(fact.relations[0].term1.relations) != 0 \
                        and fact.relations[0].term1.relations[0].operator == ';':
                            # this require goal is true only if all other are false
                            # example: tall(abc); short(abc) :- human(abc)
                            # if not(short(abc)), then tall(abc) must be true
                            expList = fact.relations[0].term1.getSubexpList()
                            required = True
                            existGoal = False
                            for exp in expList:
                                if exp.contains.ss != self.contains.ss:
                                    for f in facts:
                                        if f != fact and f.contains != None:
                                            if f.ss == self.contains.ss:
                                                required = False
                                                break
                                            # unify
                                            sub = {}
                                            res, f.contains, self.contains = safe_unify(f.contains, self.contains, sub)
                                            if res:
                                                if (self.contains.ss == substitute(sub, f.contains).ss):
                                                    required = False
                                                    break
                                elif exp.ss == self.contains.ss:
                                    existGoal = True
                            if required and existGoal:
                                if fact.relations[0].term2.getValue(facts, rules, atomList):
                                    return True
        elif self.type == CONST_FACT and self.contains == None:
            if self.relations[0].operator == ":-":
                if self.relations[0].term2.getValue(facts, rules, atomList):
                    if (self.relations[0].term1.getValue(facts, rules, atomList)):
                        return True
                else:
                    return True
            elif self.relations[0].operator == ",":
                varList = self.getVariableList()
                if len(varList) == 0:
                    if (all(term.getValue(facts, rules, atomList) for term in self.getSubexpList())):
                        return True
                else:
                    reList = []
                    varSett = set()
                    for term in self.getSubexpList():
                        var = term.getVariableList()
                        if len(var) != 0:
                            for v in var:
                                varSett.add(v)
                            re = term.findAllSubstitute(facts, rules, atomList)
                            if len(re) == 0:
                                reList = []
                                break
                            reList.append(re)
                    if len(reList) != 0:
                        merg = mergeAndSubs(reList, varSett)
                        for r in merg:
                            if substituteExp(r, self).getValue(facts, rules, atomList):
                                return True
            elif self.relations[0].operator == ";":
                if (any(term.getValue(facts, rules, atomList) for term in self.getSubexpList())):
                    return True
            elif self.relations[0].operator == "=":
                if (self.relations[0].term1.ss == self.relations[0].term2.ss):
                    return True
            elif self.relations[0].operator == "\\=":
                if (self.relations[0].term1.ss != self.relations[0].term2.ss):
                    return True
        
        # check rules
        if self.contains != None:
            for rule in rules:
                sub = {}
                res, rule.consequent, self.contains = safe_unify(rule.consequent, self.contains, sub)
                if res:
                    newStr = rule.antecedent[0].ss
                    for i in range(1, len(rule.antecedent)):
                        newStr += ", " + rule.antecedent[i].ss
                    anteExp = Expression(newStr)
                    if substituteExp(sub, anteExp).getValue(facts, rules, atomList):
                        return True
        return False
    
    def findAllSubstitute(self, facts:list, rules:list, atomList:list) -> list[dict]:
        subs = []
        # check facts
        if self.type == CONST_FACT and self.contains != None:
            if self.contains.functor == "not":
                innerRes = Expression(self.contains.arguments[0].ss).findAllSubstitute(facts, rules, atomList)
                varr = self.getVariableSet()
                allSub = getAll(varr, atomList)
                for ir in innerRes:
                    for ind, asub in enumerate(allSub):
                        if not differentSub(asub, ir, varr):
                            allSub.pop(ind)
                subs = allSub
            else:
                for fact in facts:
                    if fact.contains != None:
                        # unify
                        sub = {}
                        res, fact.contains, self.contains = safe_unify(fact.contains, self.contains, sub)
                        if res:
                            subs.append(sub)
                    elif haveSameFunctors(fact, self) and len(fact.getVariableSet()) == len(self.getVariableSet()):
                        subs = getAll(self.getVariableSet(), atomList)
                    elif fact.relations[0].operator == ':-':
                        # unify
                        sub = {}
                        res, fact.relations[0].term1, self.contains = safe_unify(fact.relations[0].term1, self.contains, sub)
                        if res:
                            re = fact.relations[0].term2.findAllSubstitute(facts, rules, atomList)
                            for s in re:
                                subs.append(s)
        elif self.type == CONST_FACT and self.contains == None:
            if self.relations[0].operator == ":-":
                re = self.relations[0].term2.findAllSubstitute(facts, rules, atomList)
                if len(re) == 0:
                    sub = getAll(self.getVariableSet(), atomList)
                else:
                    subs = re
            elif self.relations[0].operator == ",":
                diffAndEqual = []
                newExp = ""
                for ind, term in enumerate(self.getSubexpList()):
                    if term.contains == None and (term.relations[0].operator == "=" or term.relations[0].operator == "\\="):
                        diffAndEqual.append(term.relations[0])
                    else:
                        if len(newExp) == 0:
                            newExp += term.ss
                        else:
                            newExp += ", " + term.ss
                self = Expression(newExp)
                reList = []
                for term in self.getSubexpList():
                    re = term.findAllSubstitute(facts, rules, atomList)
                    if len(re) == 0:
                        reList = []
                        break
                    reList.append(re)
                if len(reList) != 0:
                    goalVarList = self.getVariableSet()
                    ree = mergeAndSubs(reList, goalVarList)
                    for r in ree:
                        allValid = True
                        for rela in diffAndEqual:
                            left = right = ""
                            for k, v in r.items():
                                if left == "":
                                    if k.ss == rela.term1.ss:
                                        left = v.ss
                                elif k.ss == rela.term2.ss:
                                    right = v.ss
                                    if rela.operator == "=":
                                        if left != right:
                                            allValid = False
                                            break
                                    else:
                                        if left == right:
                                            allValid = False
                                            break
                            if not allValid:
                                break   
                        if allValid:
                            thayThe = substituteExp(r, self)
                            if thayThe.getValue(facts, rules, atomList):
                                newR = {}
                                for kk, vv in r.items():
                                    if kk.ss in goalVarList:
                                        newR[kk] = vv
                                notin = True
                                for su in subs:
                                    if not differentSub(su, newR, goalVarList):
                                        notin = False
                                        break
                                if notin:                           
                                    subs.append(newR)
            elif self.relations[0].operator == ";":
                reList = []
                for term in self.getSubexpList():
                    re = term.findAllSubstitute(facts, rules, atomList)
                    reList.append(re)
                subs = mergeAndSubs(reList, self.getVariableSet())
            elif self.relations[0].operator == "=":
                subs = findEqual(self.getVariableSet(), atomList)
            elif self.relations[0].operator == "\\=":
                subs = findDiff(self.getVariableSet(), atomList)
        
        # check rules
        goalVarList = self.getVariableList()
        for ind in range(len(rules)):
            res, newRule = standardizeVariable(rules[ind], self, goalVarList)
            if res:
                newStr = newRule.antecedent[0].ss
                for i in range(1, len(newRule.antecedent)):
                    newStr += ", " + newRule.antecedent[i].ss
                anteExp = Expression(newStr)
                ress = anteExp.findAllSubstitute(facts, rules, atomList)
                for r in ress:
                    notin = True
                    for s in subs:
                        if not differentSub(s, r, goalVarList):
                            notin = False
                            break
                    if notin:
                        sub = {}
                        for k, v in r.items():
                            if k.ss in goalVarList:
                               sub[k] = v
                        subs.append(sub) 
        return subs

def substituteExp(sub, exp:Expression): # applying substitution sigma to sentence
    tempExp = Expression(exp.ss)
    if sub == None or len(sub) == 0:
        return tempExp
    elif exp.type == CONST_FACT and exp.contains != None:
        tempExp.contains = substitute(sub, exp.contains)
        tempExp.ss = tempExp.updateNewStr()
        return tempExp
    elif exp.type == CONST_FACT:
        for ind in range(0, len(exp.relations), 2):
            # since we use binary relations, jump 2 index each time to reduce unnecessary steps
            tempExp.relations[ind].term1 = substituteExp(sub, exp.relations[ind].term1)
            tempExp.relations[ind].term2 = substituteExp(sub, exp.relations[ind].term2)
        if len(exp.relations) % 2 == 0: # last relation
            tempExp.relations[len(exp.relations) - 1].term2 = substituteExp(sub, exp.relations[len(exp.relations) - 1].term2)
        tempExp.ss = tempExp.updateNewStr()
        return tempExp
    elif exp.type == CONST_RULE:
        tempExp.contains.consequent = substitute(sub, exp.contains.consequent)
        for ind in range(len(exp.contains.antecedent)):
            tempExp.contains.antecedent[ind] = substituteExp(sub, exp.contains.antecedent[ind])
        tempExp.ss = tempExp.updateNewStr()
        return tempExp
    else:
        return tempExp
