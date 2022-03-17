def ret( positions, length ):
    starts = length - positions[0] 
    ans = set()
    if len(positions)==1: 
        ans = { ( "." * i + "#" * positions[0] + "." * (starts-i) ) for i in range( starts+1 ) }
    else:
        for i in range(length-positions[0]): 
            for sol in ret(positions[1:],starts-i-1):
                ans.add( "." * i + "#" * positions[0] + "." + sol )
    return ans

def combinations( rowsInfo, h, w ):
    return [ ret( rowsInfo[i], h ) for i in range(w) ]

def checkfields(  positions, length ):
    a = [ set() for _ in range( length ) ]
    for pos in positions:
        for i in range( len( pos ) ):
              a[i].add( pos[i] )
    return a 

def delete( rowstocheck, clostocheck, w, h ):
    for i in range(7):
        nextIter = False
        for rid in range(len(rowstocheck)): 
            checkedrow = checkfields(rowstocheck[rid], h) 
            for coll in range(len(checkedrow)): 
                if(len( checkedrow[coll] ) == 1): 
                    (char,) = checkedrow[coll]    
                    d = []
                    for p in clostocheck[coll]: 
                        if( p[rid] != char):
                            d.append(p)
                    for dd in d:
                        clostocheck[coll].remove( dd )
        for cid in range(len(clostocheck)):
            checkedcol = checkfields( clostocheck[cid], w )
            for roww in range(len(checkedcol)):
                if (len(checkedcol[roww]) == 1):
                    (char,) = checkedcol[roww]
                    d = []
                    for p in rowstocheck[roww]:
                        if( p[cid] != char ):
                            d.append(p)
                    for dd in d:
                        rowstocheck[roww].remove( dd )
        if( any( [len(x) == 0 for x in rowstocheck] ) or any( len(x) == 0 for x in clostocheck ) ):
            return False 

    if( all( [len(x) == 1 for x in rowstocheck] ) ):
        return ( True, rowstocheck )
    return (rowstocheck,clostocheck)

def backtr( back, now, next, i, cols ):
    if i > maxDepth:
        return False
    for poss in now:
        nextval = [ [ b for b in a ] for a in next ]
        nexted = [ [ b for b in a ] for a in cols ]
        res = delete( back + [{poss}] + nextval, nexted, nw, nh )
        if res == False:
            continue
        if res[0] == True:
            return res[1]
        a = back + [{poss}]
        b = res[0][i]
        c = res[0][(i+1):]
        res = backtr( a, b , c , i + 1, res[1] )
        if res != False:
            return res
    return False

def count(row):
    count = []
    l = 0
    for i in range(len(row)):
        if(row[i] == '#'):
            l += 1
        elif(l != 0):
            count.append( l )
            l = 0
    if(row[len(row) - 1] == '#'):
        count.append(l)
    return count

def perm(tab):
    p = set()
    for el in tab:
        if len(p) == 0:
            for e in el:
                p.add(e)
        else:
            a = set()
            for e in el:
                for pp in p:
                    a.add(pp +" "+ e)
            p = a
    a = []
    for el in p:
        h = el.split(" ")
        a.append(h)
    return a           

def findgood(betterrows, cols, w):
    for el in betterrows:
        it = 0
        for i in range(w):
            string = ''
            for j in range(len( el )):
                string += el[j][i]
            if(count(string) == cols[i]):
                it = it + 1
        if(it == w):
            return el

with open("zad_input.txt", "r") as in_f:
    with open("zad_output.txt", "w") as out_f:
        w, h = [int(x) for x in next(in_f).split()]
        r = [[int(el) for el in line.split()] for line in in_f]
        rows, cols = r[:w], r[w:]
        nh = h
        nw = w
        maxDepth = h
        rowstocheck = combinations(rows, h, w)
        colstocheck = combinations(cols, w, h)
        (betterrows,bettercols) = delete(rowstocheck, colstocheck, w, h)
        odp = backtr( [], betterrows[0], betterrows[1:], 1, bettercols )
        pr = ''
        for ell in odp:
            for  el in ell:
                pr = pr + el + '\n'
        out_f.write(pr)
