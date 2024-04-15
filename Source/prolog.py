from expression import *

SPECIALCHAR = "_VarAtom"
    
class Prolog:
    def __init__(self, facts:list[Expression] = [], rules:list[Rule] = [], atoms:list[str] = []):
        self.facts = facts
        self.rules = rules
        self.atoms = atoms

    def copyy(self):
        fac = list[Expression]()
        ru = list[Rule]()
        at = list[str]()
        for f in self.facts:
            fac.append(Expression(f.ss))
        for r in self.rules:
            ru.append(Expression(r.ss).contains)
        at = self.atoms.copy()
        return fac, ru, at
    
    def add_fact(self, fact):
        self.facts.append(fact)

    def add_rule(self, rule):
        self.rules.append(rule)

    def readKB(self, fileName:str):
        try:
            file = open(fileName, 'r')
        except IOError:
            return False
        
        self.facts.clear()
        self.rules.clear()
        self.atoms.clear()
        lines = str(file.read()).split(".")
        for line in lines:
            line = line.replace('\n', "")
            if line == "" or lines == " ":
                continue
            line = line.strip()
            sentence = Expression(line)
            if sentence.type == CONST_FACT:
                # split 'and' relation into seperated facts
                if len(sentence.relations) != 0 and sentence.relations[0].operator == ',':
                    expList = sentence.getSubexpList()
                    for exp in expList:
                        self.add_fact(exp)
                else:
                    self.add_fact(sentence) 
            else:
                self.add_rule(sentence.contains)
                
            atom = sentence.getAllAtom()
            for a in atom:
                if a not in self.atoms:
                    self.atoms.append(a)
        file.close()
        return True
            
    def query(self, goal:Expression):
        # if there are any variable -> find substitution
        varSet = goal.getVariableSet()
        if len(varSet) != 0:
            # if len(varSet) >= 3:
            # replace atom with some special variables
            atos = goal.getVariableList(CONST_ATOM)
            if len(atos) >= 1:
                oldG = Expression(goal.ss)
                stin = goal.ss
                specs = []
                for a in atos:
                    newVar = str(SPECIALCHAR + a)
                    specs.append(newVar)
                    stin = stin.replace(a, newVar)
                goal = Expression(stin)
                
            tempRs = goal.findAllSubstitute(self.facts, self.rules, self.atoms)

            
            res = []
            # go back to original string
            if len(atos) >= 1:
                for r in tempRs:
                    allValid = True
                    for k, v in r.items():
                        if k.ss.startswith(SPECIALCHAR):
                            if v.ss != k.ss[len(SPECIALCHAR):]:
                                allValid = False
                                break
                    if allValid:
                        subadd = {}
                        for k, v in r.items():
                            if k.ss not in specs:
                                subadd[k] = v
                        res.append(subadd)
                goal = oldG
            else:
                res = tempRs
            for sub in res:
                printSubstitute(sub)
            # else:
            #     subs = []
            #     maxSubs = len(varSet) ** len(self.atoms)
            #     while True:
            #         sub = {}
            #         for v in varSet:
            #             sub[Term(v)] = Term(random.choice(self.atoms))
            #         notin = True
            #         for s in subs:
            #             if not differentSub(s, sub, varSet):
            #                 notin = False
            #                 break
            #         if notin:
            #             subs.append(sub)
            #             if substituteExp(sub, goal).getValue(self.facts, self.rules, self.atoms):
            #                 printSubstitute(sub)
            #             if len(subs) == maxSubs:
            #                 break
            return False
        else: # else check the truth of the goal
            return goal.getValue(self.facts, self.rules, self.atoms) # using backward chaining
