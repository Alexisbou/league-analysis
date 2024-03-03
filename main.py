import roster
import pandas as pd
import datetime as dt

if __name__ == '__main__':

    start_dt = dt.date.today() - dt.timedelta(days=10)
    end_dt = dt.date.today()
    res = roster.fetch_picks_and_bans(start_dt,end_dt)

    df = pd.DataFrame()
    print('d')
    # grouped = games_df.groupby('GameId')

    for item in res:
        game = item['title']
        df = df._append(game,ignore_index=True)

    print('done')

