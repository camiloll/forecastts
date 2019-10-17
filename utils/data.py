import numpy as np
import pandas as pd
from json import dumps
from sympy import Symbol, Poly, solve_poly_system


def process(file, ext):
    if ext == '.csv':
        df = pd.read_csv(file)  
    else:
        df = pd.read_excel(file)
    
    t = df[df.columns[0]].to_list()
    ts = df[df.columns[1]].to_list()
    
    data = {'ts':ts,'t':t}
    return dumps(data)

def restricted():
    pass


def ψ(H, Φ, Θ):

    L = Symbol('L')
 
    syms = []

    for i in range(H,-1,-1):

        syms.append(Symbol('ψ_{}'.format(i)))

 

    Z = Poly(syms,L)

    AR = Poly([-1*φ for φ in reversed(Φ)]+[1],L)

    MA = Poly([-1*θ for θ in reversed(Θ)]+[1],L)

 

    S = (AR*Z-MA).all_coeffs()

    ψ_ = solve_poly_system(S[len(S)-H-1:])[0]

    M = np.empty((H,H))

 

    for i in range(H):

        for j in range(H):

            M[i,j] = -1*ψ_[i-j] if i>j-1 else 0

    

    return M