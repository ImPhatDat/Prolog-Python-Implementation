male(phillip).
male(charles).
male(mark).
male(timothy).
male(andrew).
male(edward).
male(william).
male(harry).
male(peter).
male(mike).
male(james).
male(george).

female(elizabeth).
female(diana).
female(camilla).
female(anne).
female(sarah).
female(sophie).
female(kate).
female(autumn).
female(zara).
female(beatrice).
female(eugenie).
female(louise).
female(charlotte).
female(savannah).
female(isla).
female(mia).

parent(elizabeth, anne).
parent(elizabeth, andrew).
parent(elizabeth, edward).
parent(elizabeth, charles).
parent(phillip, charles).
parent(phillip, anne).
parent(phillip, andrew).
parent(phillip, edward).

parent(diana, william).
parent(diana, harry).
parent(charles, william).
parent(charles, harry).

parent(anne, peter).
parent(anne, zara).
parent(mark, peter).
parent(mark, zara).

parent(andrew, beatrice).
parent(andrew, eugenie).
parent(sarah, beatrice).
parent(sarah, eugenie).

parent(edward, louise).
parent(edward, james).
parent(sophie, louise).
parent(sophie, james).

parent(william, george).
parent(william, charlotte).
parent(kate, george).
parent(kate, george).

parent(peter, savannah).
parent(peter, isla).
parent(autumn, savannah).
parent(autumn, isla).

parent(zara, mia).
parent(mike, mia).

married(elizabeth, phillip).
married(charles, camilla).
married(anne, timothy).
married(edward, sophie).
married(william, kate).
married(peter, autumn).
married(zara, mike).

divorced(diana,charles).
divorced(mark, anne).
divorced(andrew, sarah).

husband(Person, Wife) :- male(Person), female(Wife), married(Person, Wife).
wife(Person, Husband) :- male(Husband), female(Person), married(Person, Husband).

father(Parent, Child) :- male(Parent), parent(Parent, Child).
mother(Parent, Child) :- female(Parent), parent(Parent, Child).

child(Child, Parent) :- parent(Parent, Child).
son(Child, Parent) :- child(Child, Parent), male(Child).
daughter(Child, Parent) :- child(Child, Parent), female(Child).

grandparent(GP, GC) :- parent(GP, P), parent(P, GC).
grandchild(GC, GP) :- grandparent(GP, GC).
grandfather(GF, GC) :- male(GF), grandparent(GF, GC).
grandmother(GM, GC) :- female(GM), grandparent(GM, GC).
grandson(GS,  GP) :- male(GS), grandchild(GS, GP).
granddaughter(GD, GP) :- female(GD), grandchild(GD, GP).

sibling(Person1, Person2) :- parent(P, Person1), parent(P, Person2), Person1 \= Person2.

brother(Person, Sibling) :- male(Person), sibling(Person, Sibling).
sister(Person, Sibling) :- female(Person), sibling(Person, Sibling).

uncle(Person, NieceNephew) :- brother(Person, Sibling), parent(Sibling, NieceNephew).
uncle(Person, NieceNephew) :- father(Parent, NieceNephew), sibling(Parent, Wife), married(Person, Wife), not(brother(Person, Parent)).
aunt(Person, NieceNephew) :- sister(Person, Sibling), parent(Sibling, NieceNephew).
aunt(Person, NieceNephew) :- mother(Parent, NieceNephew), sibling(Parent, Husband), married(Husband, Person), not(sister(Person, Parent)).

nephew(Person, AuntUncle) :- uncle(AuntUncle, Person), male(Person).
nephew(Person, AuntUncle) :- aunt(AuntUncle, Person), male(Person).
niece(Person, AuntUncle) :- uncle(AuntUncle, Person), female(Person).
niece(Person, AuntUncle) :- aunt(AuntUncle, Person), female(Person).