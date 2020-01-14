import pandas as pd
from fbprophet import Prophet


def get():
    df = pd.DataFrame()

    for month in range(1, 13):
        _df = pd.read_csv("social_bakers_twitter_2019_{}月.csv".format(month))
        df = pd.concat([df, _df]).fillna(0)

    df['ds'] = df['年'].astype(str) + '-' + df['月'].str.replace('月', '')

    def _get(name):
        if df[name].dtype == 'object':
            df[name] = df[name].str.replace('%', '')

        _df = df.loc[:, ['ds', name]].rename(columns={
            name: 'y'
        })
        # _df['y'] = _df['y'].astype(int)
        # 欠損値の補正
        # _df.loc[_df['y'] == 0, 'y'] = _df['y'].mean()
        return _df

    return _get


def show(df, is_show=True):
    # m = Prophet(seasonality_mode='multiplicative').fit(df)
    m = Prophet(seasonality_mode='multiplicative', mcmc_samples=300).fit(df)
    future = m.make_future_dataframe(periods=365)
    fcst = m.predict(future)
    fig1 = m.plot(fcst)
    if is_show:
        fig1.show()
    # fig2 = m.plot_components(fcst)
    # fig2.show()

    return fcst


def run(title, f):
    df = f(title)
    fcst = show(df)

    # 予測データの保存
    fcst.to_csv('予測{}.csv'.format(title))

    # 月ごとの集計
    fcst = fcst.set_index('ds')
    fcst.resample(rule="M").mean().to_csv('予測-(月){}.csv'.format(title))

if __name__ == '__main__':
    f = get()

    run('平均フォロワー', f)
    run('平均インタラクション', f)
    run('リツイート率', f)
    run('いいね率', f)
    run('返信率', f)

