from prolog import *

def main():
    
    prolog = Prolog()
    print("NOTE: After reading the KB, every changes to the KB won't be updated until you open it again.")
    print("      Enter 'back' to go back to previous task or exit.")
    while True:
        fileName = str(input("\nEnter the name or path of the knowledges base (*.pl): "))
        if fileName == "back":
            print("Thanks for using")
            break
        if fileName[-3:] != ".pl":
            fileName += ".pl"
        if not prolog.readKB(fileName):
            print("Cannot open KB file, please try again")
            continue
        
        proTemp = Prolog()
        proTemp.facts, proTemp.rules, proTemp.atoms = prolog.copyy()
        
        print("\nEnter queries")
        while True:
            st = str(input("\n?- "))
            if st == "back":
                break
            if st.find(SPECIALCHAR) != -1:
                print("Syntax error, the keyword " + SPECIALCHAR + " has been used")
                continue
            if len(st) != 0 and st[-1] == ".":
                st = st[:-1]
            exp = Expression(st)
            if exp.type == None:
                print("Syntax error, the query can't be represented correctly")
                continue
            sol = prolog.query(exp)
            print(sol)
            prolog.facts, prolog.rules, prolog.atoms = proTemp.copyy()

if __name__ == '__main__':
    main()