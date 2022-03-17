def B(i,j):
    return 'B_%d_%d' % (i,j)

def row(j, w):
    return [B(i,j) for i in range(w)]

def col(i, h):
    return [B(i,j) for j in range(h)]

def squares(w, h):
    return [[B(i,j), B(i+1,j), B(i,j+1), B(i+1,j+1)] for j in range(h-1) for i in range(w-1)]

def rows(w, h):
    return [[B(i,j), B(i+1,j), B(i+2,j)] for i in range(w-2) for j in range(h)]

def cols(w, h):
    return [[B(i,j), B(i,j+1), B(i,j+2)] for i in range(w) for j in range(h-2)]

def storms(rows_input, cols_input, triples):
    writeln(':- use_module(library(clpfd)).')
    
    w = len(rows_input)
    h = len(cols_input)
    
    bs = [ B(i,j) for i in range(w) for j in range(h)]
    
    writeln('solve([' + ', '.join(bs) + ']) :- ')
    possible_row = [[0,0,0], [0,0,1], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1]]
    possible_sq = [[0,0,0,0], [0,0,0,1], [0,0,1,0], [0,0,1,1], [0,1,0,0], [0,1,0,1], [1,0,0,0], [1,0,1,0], [1,1,0,0], [1,1,1,1]]
    
    for b in bs:
        output.write(f'    {b} in 0..1, ')
    for s in squares(w, h):
        writeln(f'    tuples_in([[{", ".join(s)}]], {possible_sq}), ')
    for c in cols(w, h):
        writeln(f'    tuples_in([[{", ".join(c)}]], {possible_row}), ')
    for r in rows(w, h):
        writeln(f'    tuples_in([[{", ".join(r)}]], {possible_row}), ')
    for j in range(h):
        writeln(f'    {" + ".join(row(j, w))} #= {cols_input[j]},')
    for i in range(w):
        writeln(f'    {" + ".join(col(i, h))} #= {rows_input[i]},')
    for c in triples:
        writeln(f'    {B(c[0], c[1])} #= {c[2]},')

    writeln('    labeling([ff], [' +  ', '.join(bs) + ']).' )
    writeln('')
    writeln(":- tell('prolog_result.txt'), solve(X), write(X), nl, told.")

def writeln(s):
    output.write(s + '\n')

txt = open('zad_input.txt').readlines()
output = open('zad_output.txt', 'w')

rows_input = list(map(int, txt[0].split()))
cols_input = list(map(int, txt[1].split()))
triples = []

for i in range(2, len(txt)):
    if txt[i].strip():
        triples.append(list(map(int, txt[i].split())))
storms(rows_input, cols_input, triples)