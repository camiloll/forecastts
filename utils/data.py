import numpy as np
import pandas as pd
import pmdarima as pm

from json import dumps, loads
from numpy.linalg import inv
from datetime import timedelta
from sympy import Symbol, Poly, solve_poly_system
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.tools import diff


def process(file, ext, log, H, C, Y, toggle, P, D, Q):
    if ext == '.csv':
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    df = df[df.columns[0]]

    if log == 'true':
        df = np.log(df).replace(-np.inf, 0)

    Zt = df.to_json(orient='values')
    t = dumps([x for x in range(len(df))])

    if toggle == 'on':
        _, Zh, th, Zh_l, Zh_u, summary = forecast(df, H)
    else:
        _, Zh, th, Zh_l, Zh_u, summary = forecastARIMA(df, H, P, D, Q)

    Zh_res = restricted_forecast(
        Zh, H, C, Y, summary['order'], summary['params'])
    data = {'Z': Zt, 't': t, 'Zh': Zh, 'th': th, 'Zh_l': Zh_l, 'Zh_u': Zh_u,
            'Zh_res': Zh_res, 'summary': dumps(summary)}

    return dumps(data)


def forecast(df, H):
    model = pm.auto_arima(df.values[:], start_p=2, start_q=2,
                          test='adf',       # use adftest to find optimal 'd'
                          max_p=5, max_q=5,  # maximum p and q
                          m=1,              # frequency of series
                          d=None,           # let model determine 'd'
                          seasonal=False,   # No Seasonality
                          start_P=0,
                          D=0,
                          trend=None,
                          with_intercept=False,
                          trace=False,
                          error_action='ignore',
                          suppress_warnings=True,
                          stepwise=True)

    # Forecast
    n_periods = H
    fc, confint = model.predict(n_periods=n_periods, return_conf_int=True)
    index_of_fc = pd.RangeIndex(start=df.index.stop, stop=df.index.stop + H)

    th = dumps([x for x in range(len(df), len(df)+H)])
    # index_of_fc = pd.PeriodIndex((pd.to_datetime(df.values[:,0]) + H*timedelta(weeks=12))[-H:],freq='Q')

    fc_series = pd.Series(fc, index=index_of_fc).to_json(orient='values')
    lower_series = pd.Series(
        confint[:, 0], index=index_of_fc).to_json(orient='values')
    upper_series = pd.Series(
        confint[:, 1], index=index_of_fc).to_json(orient='values')

    model_params = model.to_dict()
    summary = {'order': model_params['order'], 'params': model_params['params'].tolist(
    ), 'summary': model.summary().as_html()}

    try:
        pred = model.predict(df.index.stop,
                             df.index.stop + H - 1,
                             typ='linear').tolist()
    except Exception:
        pred = model.predict(df.index.stop,
                             df.index.stop + H - 1).tolist()

    pred_series = pd.Series(pred).to_json(orient='values')

    return pred_series, fc_series, th, lower_series, upper_series, summary


def forecastARIMA(df, H, P, D, Q):
    order = (P, D, Q)
    model = ARIMA(df.values[:], order=order).fit(trend='nc')

    # Forecast
    n_periods = H
    fc, se, confint = model.forecast(n_periods)
    index_of_fc = pd.RangeIndex(start=df.index.stop, stop=df.index.stop+H)
    th = dumps([x for x in range(len(df), len(df)+H)])
    # index_of_fc = pd.PeriodIndex((pd.to_datetime(df.values[:,0]) + H*timedelta(weeks=12))[-H:],freq='Q')

    fc_series = pd.Series(fc, index=index_of_fc).to_json(orient='values')
    lower_series = pd.Series(
        confint[:, 0], index=index_of_fc).to_json(orient='values')
    upper_series = pd.Series(
        confint[:, 1], index=index_of_fc).to_json(orient='values')

    summary = {'order': order,
               'params': list(model.arparams)+list(model.maparams),
               'summary': model.summary().as_html()}

    try:
        pred = model.predict(df.index.stop,
                             df.index.stop + H - 1,
                             typ='linear').tolist()
    except Exception:
        pred = model.predict(df.index.stop,
                             df.index.stop + H - 1).tolist()

    pred_series = pd.Series(pred).to_json(orient='values')

    return pred_series, fc_series, th, lower_series, upper_series, summary


def restricted_forecast(Zh, H, C, Y, order, params):
    print('ARIMA: ', order)
    params = np.round(params, 5).tolist()
    print(params)

    C = np.array(loads(C), dtype=np.double)
    print('C')
    print(C)

    Ct = np.transpose(C)

    Y = np.array(loads(Y), dtype=np.double)
    print('Y')
    print(Y)

    Φ = params[:order[0]]
    print('Φ: ', Φ)

    Θ = params[(len(params) - order[-1]):]
    print('Θ: ', Θ)

    PSI = ψ(H, Φ, Θ)
    print('PSI')
    print(PSI)

    PSIt = np.transpose(PSI)
    A = PSI @ PSIt @ Ct @ inv(C @ PSI @ PSIt @ Ct)
    print('A')
    print(A)

    Zf = np.array(loads(Zh), dtype=np.double)
    Zh_res = Zf + A@(Y - C@Zf)

    return dumps(Zh_res.tolist())


def ψ(H, Φ, Θ):

    L = Symbol('L')

    syms = []

    for i in range(H, -1, -1):
        syms.append(Symbol('ψ_{}'.format(i)))

    Z = Poly(syms, L)

    AR = Poly([-1*φ for φ in reversed(Φ)]+[1], L)

    MA = Poly([-1*θ for θ in reversed(Θ)]+[1], L)

    S = (AR*Z-MA).all_coeffs()

    if len(Θ) == 0 and len(Φ) == 1:
        ψ_ = [Φ[0]**k for k in range(H)]

    elif len(Θ) == 1 and len(Φ) == 1:
        ψ_ = [1]+np.round([Φ[0]**k*(Φ[0]-Θ[0])
                           for k in range(H-1)], 5).tolist()
    else:
        ψ_ = solve_poly_system(S[len(S)-H-1:])[0]

    M = np.empty((H, H))

    for i in range(H):
        for j in range(H):
            M[i, j] = -1*ψ_[i-j] if i > j-1 else 0

    return np.array(M, dtype=np.double)
