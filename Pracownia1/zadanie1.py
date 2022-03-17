
def ruchy(krol):
    x = krol[0]
    y = krol[1]
    ruchy = []
    for i in range(-1,2):
        for j in range(-1,2):
            if (((97 <= (ord(x) + j) and (ord(x) + j) <= 104)) and ((56 >= (ord(y) + i) and (ord(y) + i) >= 49)) and not(i == 0 and j == 0) ):
                ruchy.append(chr(ord(x) + j) + chr(ord(y) + i))
    return ruchy

def ruchykrol(ruch, bk , bw , ck):
    if ruch == 'white':
        swoj = ruchy(bk)
        przeciwnik = ruchy(ck)
        return [ x for x in swoj if (x not in przeciwnik) and ( x != bw ) ]
    else:
        swoj = ruchy(ck)
        przeciwnik = ruchy(bk)
        return [ x for x in swoj if (x not in przeciwnik)
            and ( x[0] != bw[0] and x[1] != bw[1] ) ]

def ruchywierzy(bk, bw , ck):
    x = bw[0]
    y = bw[1]
    j = 1
    wynik = []
    while ord(x) + j <= 104 and (ord(x) + j != ord(bk[0]) or ord(y) != ord(bk[1])):
        wynik.append(chr(ord(x) + j) + y)
        j = j + 1
    j = 1
    while ord(x) - j >= 97 and (ord(x) - j != ord(bk[0]) or ord(y) != ord(bk[1])):
        wynik.append(chr(ord(x) - j) + y)
        j = j + 1
    j = 1
    while ord(y) + j <= 56 and (ord(x) != ord(bk[0]) or ord(y) + j != ord(bk[1])):
        wynik.append(x + chr(ord(y) + j))
        j = j + 1
    j = 1
    while ord(y) - j >= 49 and (ord(x) != ord(bk[0]) or ord(y) - j != ord(bk[1])):
        wynik.append(x + chr(ord(y) - j))
        j = j + 1
    return wynik

def szukajszacha(ruch, bk , bw , ck):
    if( ruchykrol( 'black', bk , bw , ck ) == [] and ( ck[0] == bw[0] or ck[1] == bw[1] ) ):
        return 0
    zapamietane = set()
    sprawdzane = []
    sprawdzane.insert(0,(bk,bw,ck, f''))
    i = 1
    while True:
        # nastepne = set()
        if ruch == 'white':
            val = sprawdzane[len(sprawdzane)-1]
            nbk = val[0]
            nbw= val[1]
            nck= val[2]
            droga= val[3]
            sprawdzane.pop()
            wierzaruchy = ruchywierzy(nbk,nbw,nck)
            for wierza in wierzaruchy:
                if f'{nbk} {wierza} {nck}' in zapamietane:
                    continue
                zapamietane.add( f"{nbk} {wierza} {nck}")
                ucieczka = ruchykrol('black',nbk,wierza,nck)
                if ucieczka == []:
                    if( (nck[0] == wierza[0] or nck[1] == wierza[1]) and wierza not in ruchy(nck)): 
                        return (droga + f'{nbw}{wierza} ' )
                else:
                    if wierza not in ruchy(nck):
                        sprawdzane.insert(0, ( nbk, wierza, nck, droga + f'{nbw}{wierza} ' ) )
            krolruchy = ruchykrol('white',nbk,nbw,nck)
            for krol in krolruchy:
                if f'{krol} {nbw} {nck}' in zapamietane:
                    continue                    
                zapamietane.add(f"{krol} {nbw} {nck}")
                ucieczka = ruchykrol('black',krol,nbw,nck)
                if ucieczka == []:
                    if( nck[0] == nbw[0] or nck[1] == nbw[1] ): 
                        return (droga + f'{nbk}{krol} ' )
                else:
                    sprawdzane.insert( 0,( krol, nbw, nck, droga + f'{nbk}{krol} ' ) )
        else:   
            val = sprawdzane[len(sprawdzane)-1]
            nbk = val[0]
            nbw= val[1]
            nck= val[2]
            droga= val[3]
            sprawdzane.pop()
            krolruchy = ruchykrol('black',nbk,nbw,nck)
            for krol in krolruchy:
                if f'{nbk} {nbw} {krol}' in zapamietane:
                    continue
                zapamietane.add(f"{nbk}{nbw}{krol}")
                sprawdzane.insert(0,(nbk,nbw,krol,droga + f'{nck}{krol} '))
        j = len(sprawdzane[len(sprawdzane)-1][3].split(' '))
        if j != i:
            i = i + 1
            if ruch == 'white':
                ruch = 'black'
            else:
                ruch = 'white'

print( szukajszacha('black', 'h8', 'g7', 'a1'))
# print( szukajszacha('white', 'h6', 'a4', 'd4')) #9
# print( szukajszacha('black', 'b4', 'f3', 'e8')) #6
# print( szukajszacha('black', 'a2', 'e4', 'a4')) #8
# print( szukajszacha('white', 'a1', 'e3', 'b7')) #9
# print( szukajszacha('black', 'g8', 'h1', 'c4')) #10
# print( szukajszacha('black', 'h7', 'a2', 'f2')) #6
