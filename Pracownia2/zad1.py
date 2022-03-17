from math import prod
from time import time

def place( blocks, total ):
    if not blocks: 
        return {"-" * total}
    if blocks[0] > total: 
        return {}

    starts = total-blocks[0] #starts = 2 means possible starting indexes are [0,1,2]
    if len(blocks)==1: #this is special case
        return { ( "." * i + "#" * blocks[0] + "." * (starts-i) ) for i in range( starts+1 ) }

    ans = set()
    for i in range(total-blocks[0]): #append current solutions
        for sol in place(blocks[1:],starts-i-1): #with all possible other solutions
            ans.add( "." * i + "#" * blocks[0] + "." + sol )
    return ans

def counter( string ):
    count = []
    prev = 0
    for i in range( len( string ) ):
        if( string[i] == '#' ):
            prev += 1
        elif( prev != 0 ):
            count.append( prev )
            prev = 0
    if( string[ len(string) - 1 ] == '#' ):
        count.append( prev )
    return count

def gen_possibilities( rowNum, rowsInfo, colsNum ):
    return [ place( rowsInfo[i], colsNum ) for i in range( rowNum ) ]

def gen_permutations( tab ):
    ret = set()
    i = 1
    for comb in tab:
        new_ret = set()
        for poss in comb:
            if( len( ret ) == 0 ):
                new_ret.add( poss )
            else:
                for r in ret:
                    new_ret.add( r + " " + poss )
        ret = new_ret
        i += 1
    return list( map( lambda x: x.split( ' ' ), ret ) )

def checker( tab, correct, num ):
    for el in tab:
        flague = True
        for i in range( num ):
            string = ''
            for j in range( len( el ) ):
                string += el[j][i]
            if( counter(string) != correct[i] ):
                flague = False
                break
        if( flague ):
            return el

def formatOutput( tab ):
    out = ''
    for line in tab:
        for char in line:
            out += char
        out += '\n'
    return out

def surePossibility( poss, lth ):
    a = [ set() for _ in range( lth ) ]
    for pos in poss:
        for i in range( len( pos ) ):
              a[i].add( pos[i] )
    return a ##returns what possible fields are to put

def minimizePossibilities( rowPoss, colsPoss, colsNum, rowsNum ):
    nextIter = True
    while( nextIter ):
        nextIter = False
        for rowIdx in range( len( rowPoss ) ): #for every row
            rowPositPoss = surePossibility( rowPoss[rowIdx], colsNum ) # we find out if there is only one possibility for char

            for coll in range( len( rowPositPoss ) ): #we check on every char in this row
                if( len( rowPositPoss[coll] ) == 1 ): #if there is only possibility
                    ( char, ) = rowPositPoss[coll]    #we cross out every other possibility
                    toRemove = set()
                    for p in colsPoss[coll]: #we check every possibility for column
                        if( p[rowIdx] != char ):
                            toRemove.add( p )
                            nextIter = True
                    for delete in toRemove:
                        colsPoss[coll].remove( delete )

        for colIdx in range( len( colsPoss ) ):
            colPositPoss = surePossibility( colsPoss[colIdx], rowsNum )

            for roww in range( len( colPositPoss ) ):
                if ( len( colPositPoss[roww] ) == 1 ):
                    (char, ) = colPositPoss[roww]
                    toRemove = set()
                    for p in rowPoss[roww]:
                        if( p[colIdx] != char ):
                            toRemove.add( p )
                            nextIter = True
                    for delete in toRemove:
                        rowPoss[roww].remove( delete )

    return ( rowPoss, colsPoss )

def zad1():
    with open( 'zad_output.txt', 'w' ) as out:
        with open( 'zad_input.txt' ) as inp:
            content = inp.read().splitlines()
        rows = int( content[0].split(' ')[0] )
        cols = int( content[0].split(' ')[1] )
        rowsInp = [0] * rows
        colsInp = [0] * cols
        for i in range( 1, rows + 1 ):
                rowsInp[i - 1] = list( map( int, content[i].split( ' ' ) ) )
        for i in range( rows + 1, len( content ) ):
                colsInp[i - rows - 1 ] = list( map( int, content[i].split( ' ' ) ) )

        r = gen_possibilities( rows, rowsInp, cols )
        c = gen_possibilities( cols, colsInp, rows )
        (rB, cB) = minimizePossibilities( r, c, cols, rows )
        
        start = time()
        result = checker( gen_permutations( rB ), colsInp, cols )
        out.write( formatOutput( result ) )

if __name__ == '__main__':
    zad1()