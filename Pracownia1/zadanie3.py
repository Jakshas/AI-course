import random

def tworztalie(kto):
    dolosowania = []
    if kto == 'Figurant':
        for i in range(0,4):
            for j in range(11,15):
                dolosowania.append((j,i))
    else:
        for i in range(0,4):
            for j in range(2,10):
                dolosowania.append((j,i))
    return dolosowania

def podlicz(reka):
    kolory = []
    for i in range(0,4):
        kolory.append(0)
    figury = []
    for i in range(0,13):
        figury.append(0)
    for (i,j) in reka:
        kolory[j] = kolory[j] + 1
        figury[i-2] = figury[i-2] + 1
    return (figury,kolory)
    


def losujtalie(kto, talia):
    pom = talia.copy()
    if kto == 'Figurant':
        reka = []
        for i in range(0,5):
            kolor = random.randint(0,3)
            figura = random.randint(11,14)
            while not (figura,kolor) in pom:
                kolor = random.randint(0,3)
                figura = random.randint(11,14)
            pom.remove((figura,kolor))
            reka.append((figura,kolor))
    else:
        reka = []
        for i in range(0,5):
            kolor = random.randint(0,3)
            figura = random.randint(2,10)
            while not (figura,kolor) in pom:
                kolor = random.randint(0,3)
                figura = random.randint(2,10)
            pom.remove((figura,kolor))
            reka.append((figura,kolor))
    return reka

def licz2(figurant):
    dwujki = 0
    for i in figurant[0]:
        if i == 2:
            dwujki = dwujki + 1
    return dwujki

def liczstrit(blotkarz):
    wynik = 0
    i = 0
    while(blotkarz[0][i] == 0 ):
        i = i + 1
    while(blotkarz[0][i] == 1):
        wynik = wynik + 1
        i = i + 1
    return wynik == 5

def liczpoker(blotkarz):
    wynik = 0
    i = 0
    while(blotkarz[0][i] == 0 ):
        i = i + 1
    while(blotkarz[0][i] == 1):
        wynik = wynik + 1
        i = i + 1
    return wynik == 5 and (5 in blotkarz[1])

def sprawdzfiguranta(figurant):
    if 4 in figurant[0]:
        return 1
    if 3 in figurant[0] and 2 in figurant[0]:
        return 2
    if 3 in figurant[0]:
        return 5
    if licz2(figurant) == 2:
        return 6
    return 7
    
def sprawdzblotkarza(blotkarz):
    if liczpoker(blotkarz):
        return 0
    if 4 in blotkarz[0]:
        return 1
    if 3 in blotkarz[0] and 2 in blotkarz[0]:
        return 2
    if 5 in blotkarz[1]:
        return 3
    if liczstrit(blotkarz):
        return 4
    if 3 in blotkarz[0]:
        return 5
    if licz2(blotkarz) == 2:
        return 6
    if 2 in blotkarz[0]:
        return 7
    return 8

def sprawdz(figurant, blotkarz):
    policzonef = podlicz(figurant)
    policzoneb = podlicz(blotkarz)
    if sprawdzfiguranta(policzonef) <= sprawdzblotkarza(policzoneb):
        return 'Figurant'
    else:
        return 'Blotkarz'

def prawdopodobienstwo():
    wb = 0
    wf = 0
    taliaf = tworztalie('Figurant')
    taliab = tworztalie('Blotkarz')
    for i in range(1,100000):
        f = losujtalie('Figurant',taliaf)
        b = losujtalie('Blotkarz',taliab)
        if sprawdz(f,b) == 'Figurant':
            wf = wf + 1
        else:
            wb = wb + 1
    return (wf/100000,wb/100000)

def usunkarte(b):
    f = random.randint(2,10)
    k = random.randint(0,3)
    while (f,k) not in b:
        f = random.randint(2,10)
        k = random.randint(0,3)
    b.remove((f,k))
    return b

print(prawdopodobienstwo())