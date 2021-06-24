import sys
import copy

""""
Lambda expresiile vor fi codificate cu urm simboluri:
lx. = lambda x. din notatie (l e rezervat, nu poate aparea ll.), nu e obligatoriu spatiu dupa punct
) ( = spatiu intre paranteze = aplicare de functie
+ - / * = simboluri uzuale de functii, spatiu intre variabile = inmultire de variabile sau ceva
exemplul din model:
lx.(ly.(lx.x + z) ((lx.x x) (x + y) + x)) (lz. x y z)
Exista exception handling, dar foarte limitat (chestii de genu lx. x )) crapa).
"""""

class Env:
    def __init__(self, cr_vars):
        # variabilele de legatura curente
        self.cr_vars = cr_vars

expr = input("Scrie expresia, respectand regulile de formatare")
LEGATURA = 0
LIBERA = 1
LEGATA = 2

vars = []
envs = [] # foloseste o stiva de environments pentru a tine cont de paranteze
will_ad_leg = False
index = 1
for char in expr:
    if char == "l": # urmeaza o variabila de legatura
        will_ad_leg = True
    elif char == "(": # cand dau de o paranteza, pun un nou env, momentan identic cu cel curent, pe stiva
        if envs != []:
            cr_env = envs[-1]
            envs += [Env(copy.deepcopy(cr_env.cr_vars))]
        else:
            envs += [Env([])] # cazuri de genul (x + y) lx. x
    elif char == ")": # cand dau de o paranteza inchisa, scot ultimul env din stiva
        if envs == []:
            print("Input invalid - paranteza ) in plus!")
            sys.exit()
        envs.pop(-1)
    # e o variabila
    elif char.isalpha():
        # e variabila de legatura
        if will_ad_leg == True:
            vars += [(char, index, LEGATURA, None)]
            cr_vars = envs[-1].cr_vars if envs != [] else [] # ma uit in env sa vad daca "suprascrie" o alta variabila de legatura
            found_it = False
            for (lchar, lindex) in cr_vars:
                if lchar == char:
                    cr_vars.remove((lchar, lindex))
                    cr_vars += [(char, index)]
                    found_it = True
                    break
            if not found_it: # daca nu poate fi pusa alta variabila, o adaug ca atare in env curent
                cr_vars += [(char, index)]
            if envs != []:
                envs[-1].cr_vars = cr_vars # posibil inutil, nu s sigur cum paseaza python listele
            else:
                envs += [Env(copy.deepcopy(cr_vars))] # prima variabila de legatura intalnita
            will_ad_leg = False
        else:
            # e ori libera, ori legata
            found_it = False
            cr_vars = envs[-1].cr_vars if envs != [] else []
            for (lchar, lindex) in cr_vars: # cr_vars sunt variabilele de legatura curente
                if lchar == char:
                    vars += [(char, index, LEGATA, lindex)]
                    found_it = True
                    break
            if not found_it:
                vars += [(char, index, LIBERA, None)]
        index += 1

print("Expresia devine: ")
index = 1
sindex = 0
for char in expr:
    if char != "l" and char.isalpha():
        expr = expr[:sindex] + char + str(index) + expr[sindex + 1:]
        sindex += len(str(index)) # pt cum gestioneaza python memoria
        index += 1
    sindex += 1
print(expr)
for (char, index, flag, parent) in vars:
    if flag == LIBERA:
        print(char + str(index) + " variabila libera")
    elif flag == LEGATURA:
        print(char + str(index) + " variabila de legatura")
    else:
        prnt = vars[parent - 1]
        (pchar, pindex, pflag, pparent) = prnt
        print(char + str(index) + " variabila legata de " + pchar + str(pindex))