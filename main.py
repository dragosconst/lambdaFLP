import re
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
vars_raw =re.findall("l(.)\.", expr)
LEGATURA = 0
LIBERA = 1
LEGATA = 2

vars = []
envs = []
will_ad_leg = False
index = 1
for char in expr:
    if char == "l":
        will_ad_leg = True
    elif char == "(":
        cr_env = envs[-1]
        envs += [Env(copy.deepcopy(cr_env.cr_vars))]
    elif char == ")":
        if envs == []:
            print("Input invalid - paranteza ) in plus!")
            sys.exit()
        envs.pop(-1)
    # e o variabila
    elif char.isalpha():
        # e variabila de legatura
        if will_ad_leg == True:
            vars += [(char, index, LEGATURA, None)]
            cr_vars = envs[-1].cr_vars if envs != [] else []
            found_it = False
            for (lchar, lindex) in cr_vars:
                if lchar == char:
                    cr_vars.remove((lchar, lindex))
                    cr_vars += [(char, index)]
                    found_it = True
                    break
            if not found_it:
                cr_vars += [(char, index)]
            if envs != []:
                envs[-1].cr_vars = cr_vars # posibil inutil, nu s sigur cum paseaza python listele
            else:
                envs += [Env(copy.deepcopy(cr_vars))]
            will_ad_leg = False
        else:
            # e ori libera, ori legata
            found_it = False
            cr_vars = envs[-1].cr_vars if envs != [] else []
            for (lchar, lindex) in cr_vars:
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