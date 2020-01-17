import pandas as pd
import glob
from fbprophet import Prophet


def get():
    df = pd.DataFrame()

    for path in glob.glob('./data/*.csv'):
        df = pd.concat([df, pd.read_csv(path)])

    df['ds'] = df['年'].astype(str) + '-' + df['月'].str.replace('月', '').str.zfill(2)
    df.loc[(df['ds'] == '2019-12'), 'ds'] = '2019-12-31'
    df = df.sort_values('ds').reset_index()

    df.to_csv('merge.csv', index=False)

    def _get(name):
        if df[name].dtype == 'object':
            df[name] = df[name].str.replace('%', '')

        _df = df.loc[:, ['ds', name]].rename(columns={
            name: 'y'
        })

        return _df

    return _get


def show(df, is_show=True):
    m = Prophet(seasonality_mode='multiplicative').fit(df)
    # m = Prophet(seasonality_mode='multiplicative', mcmc_samples=300).fit(df)
    future = m.make_future_dataframe(periods=12,  freq='M')
    fcst = m.predict(future)
    fig1 = m.plot(fcst)
    # if is_show:
    #     fig1.show()
    # fig2 = m.plot_components(fcst)
    # fig2.show()

    return fcst


def show_logistic(df, cap, floor, is_show=True):
    df['cap'] = cap
    df['floor'] = floor
    # m = Prophet(growth='logistic', seasonality_mode='multiplicative', mcmc_samples=300).fit(df)
    m = Prophet(growth='logistic', seasonality_mode='multiplicative').fit(df)

    future = m.make_future_dataframe(periods=12,  freq='M')
    future['cap'] = cap
    future['floor'] = floor
    fcst = m.predict(future)
    fig1 = m.plot(fcst)
    # if is_show:
    #     fig1.show()
    # fig2 = m.plot_components(fcst)
    # fig2.show()

    return fcst


def done(fcst, df, title):
    # 予測データの保存
    fcst.to_csv('予測{}.csv'.format(title))

    # # 月ごとの集計
    # fcst = fcst.set_index('ds')
    # fcst.resample(rule="M").mean().to_csv('予測-(月){}.csv'.format(title))

    return fcst


def pattern1():
    f = get()
    KEY = '平均フォロワー'
    df = f(KEY)

    fcst = show(df)
    return done(fcst, df, KEY)

def pattern2():
    f = get()
    KEY = '平均インタラクション'
    df = f(KEY)
    fcst = show(df)

    return done(fcst, df, KEY)

def pattern3():
    f = get()
    KEY = 'リツイート率'
    df = f(KEY)
    fcst = show_logistic(df, 80, 20)

    return done(fcst, df, KEY)

def pattern4():
    f = get()
    KEY = 'いいね率'
    df = f(KEY)
    fcst = show_logistic(df, 60, 10)

    return done(fcst, df, KEY)

def pattern5():
    f = get()
    KEY = '返信率'
    df = f(KEY)
    df.loc[(df['ds'] == '2019-12-31'), 'ds'] = '2019-12'
    # 異常値を排除
    original = df
    df.loc[(df['ds'] > '2016-11-01') & (df['ds'] < '2017-08-31'), 'y'] = None
    print(df)
    fcst = show_logistic(df, 3, 0)

    return done(fcst, original, KEY)


if __name__ == '__main__':
    p1 = pattern1()
    df = pd.DataFrame({
        '作成日時': p1['ds'],
        '平均フォロワー': p1['yhat'],
        '平均インタラクション': pattern2()['yhat'],
        'リツイート率': pattern3()['yhat'],
        'いいね率': pattern4()['yhat'],
        '返信率': pattern5()['yhat'],
        '予測': False,
    })

    df.loc[(df['作成日時'] > '2020-01-01'), '予測'] = True
    df.to_csv('result.csv')
