import numpy as np
import pandas as pd
import pmdarima as pm

from json import dumps
from datetime import timedelta
from sympy import Symbol, Poly, solve_poly_system
from statsmodels.tsa.arima_model import ARIMA


def process(file, ext, H):
    if ext == '.csv':
        df = pd.read_csv(file)  
    else:
        df = pd.read_excel(file)
    
    df = df[df.columns[0]]

    Zt = df.to_json(orient='values')
    t = dumps([x for x in range(len(df))])
    Zh, th, Zh_l, Zh_u, summary = forecast(df,H)
    
    data = {'Z':Zt, 't':t, 'Zh':Zh, 'th':th, 'Zh_l':Zh_l,'Zh_u':Zh_u,'summary':summary}

    return dumps(data)


def forecast(df,H):
    model = pm.auto_arima(df.values[:], start_p=2, start_q=2,
                        test='adf',       # use adftest to find optimal 'd'
                        max_p=3, max_q=3, # maximum p and q
                        m=1,              # frequency of series
                        d=None,           # let model determine 'd'
                        seasonal=False,   # No Seasonality
                        start_P=0, 
                        D=0, 
                        trace=False,
                        error_action='ignore',  
                        suppress_warnings=True, 
                        stepwise=True)

    # Forecast
    n_periods = H
    fc, confint = model.predict(n_periods=n_periods, return_conf_int=True)
    index_of_fc = pd.RangeIndex(start=df.index.stop,stop=df.index.stop+H)
    th = dumps([x for x in range(len(df),len(df)+H)])
    # index_of_fc = pd.PeriodIndex((pd.to_datetime(df.values[:,0]) + H*timedelta(weeks=12))[-H:],freq='Q')
    
    fc_series = pd.Series(fc, index=index_of_fc).to_json(orient='values')
    lower_series = pd.Series(confint[:, 0], index=index_of_fc).to_json(orient='values')
    upper_series = pd.Series(confint[:, 1], index=index_of_fc).to_json(orient='values')

    model_params = model.to_dict()
    summary = dumps({'order':model_params['order'],'params':model_params['params'].tolist(),'summary':model.summary().as_html()})
    
    return fc_series, th, lower_series, upper_series, summary


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