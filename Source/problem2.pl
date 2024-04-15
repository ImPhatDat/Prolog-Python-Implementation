male(conan).
male(kogoro).
male(agasa).
male(heiji).
male(megure).
male(takagi).
male(yusaku).
male(gin).
male(vodka).
male(akai).
male(amuro).
male(genta).
male(mitsuhiko).

female(ran).
female(eri).
female(haibara).
female(sonoko).
female(sato).
female(yukiko).
female(vermouth).
female(sera).
female(kazuha).
female(ayumi).

child(ayumi).
child(genta).
child(mitsuhiko).

friend(conan, heiji).
friend(conan, haibara).
friend(conan, sonoko).
friend(conan, ayumi).
friend(conan, genta).
friend(conan, mitsuhiko).

friend(ran, sonoko).
friend(ran, heiji).
friend(ran, kazuha).
friend(Person1, Person2) :- love(Person1, Person2).

love(conan, ran).
love(yusaku, yukiko).
love(kogoro, eri).
love(heiji, kazuha).
love(sato, takagi).

parent(yusaku, conan).
parent(yukiko, conan).
parent(mori, ran).
parent(eri, ran).

police(megure).
police(takagi).
police(sato).
police(akai).
police(amuro).

blackOrganization(gin).
blackOrganization(vodka).
blackOrganization(vermouth).
blackOrganization(akai).
blackOrganization(amuro).

detective(conan).
detective(heiji).
detective(kogoro).
detective(sera).


spy(X) :- police(X), blackOrganization(X).

coop(X, Y) :- police(X), detective(Y).
coop(X, Y) :- police(Y), detective(X).

coop(X, Y) :- friend(X, Y), not(child(Y)), not(child(X)), X \= Y.

coop(X, Y) :- parent(Y, X).
coop(X, Y) :- parent(X, Y).

coop(X, Z) :- parent(Z, Y), friend(X, Y).
coop(X, Z) :- parent(X, Y), friend(Z, Y).

coop(X, Y) :- detective(X), detective(Y), X \= Y.
coop(X, Y) :- blackOrganization(X), blackOrganization(Y), X \= Y.

confront(X, Y) :- police(X), blackOrganization(Y), X \= Y.
confront(X, Y) :- police(Y), blackOrganization(X), X \= Y.
confront(X, Y) :- detective(X), blackOrganization(Y).
confront(X, Y) :- detective(Y), blackOrganization(X).
confront(X, Y) :- spy(X), blackOrganization(Y), X \= Y.
confront(X, Y) :- spy(Y), blackOrganization(X), X \= Y.

protect(X, Y, Z) :- police(X), female(Y), not(blackOrganization(Y)), X \= Y, blackOrganization(Z).
protect(X, Y, Z) :- detective(X), female(Y), not(blackOrganization(Y)), X \= Y, blackOrganization(Z).
protect(X, Y, Z) :- police(X), child(Y), blackOrganization(Z).
protect(X, Y, Z) :- detective(X), child(Y), blackOrganization(Z).
protect(X, Y) :- blackOrganization(X), blackOrganization(Y), X \= Y.
