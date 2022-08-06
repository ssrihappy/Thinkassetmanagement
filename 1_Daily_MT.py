import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import telegram

token = '본인 토큰을 입력'
bot = telegram.Bot(token=token)

index = ['^IXIC', '^GSPC', '^DJI', '^KS11', '^KQ11', 'BTC-USD']
ticker = ['NASDAQ', 'S&P500', 'DOW', 'KOSPI', 'KOSDAQ', 'BTC']
mt_df = pd.DataFrame(columns = ['Ticker', 'Signal', 'Score'])

def cls_prices(ticker, mvday, day):
    now = datetime.today().strftime('%Y-%m-%d')
    start = (datetime.today() - relativedelta(months=2)).strftime('%Y-%m-%d')
    close = yf.download(ticker, start=start, end=now)
    sma = close.Close.rolling(window=mvday).mean()[-1]
    price = close.Close[-day]
    return sma, price

for i in index:
    a_3 = cls_prices(i, 3, 1)[1]/cls_prices(i, 3, 1)[0] -1
    a_5 = cls_prices(i, 5, 1)[1]/cls_prices(i, 5, 1)[0] -1
    a_10 = cls_prices(i, 10, 1)[1]/cls_prices(i, 10, 1)[0] -1
    score = 0
    if a_3 and a_5 and a_10 >0:
        signal = 'Buy'
        score =+ 3
    elif (a_3 and a_5) > 0 and a_10 <0:
        signal = 'Buy'
        score =+ 1
    elif a_3 and a_5 and a_10 <0:
        signal = 'Sell'
        score =+ -3
    elif (a_3 and a_5) < 0 and a_10 >0:
        signal = 'Sell'
        score =+ -1
    else:
        signal = 'Hold'
    mt_df = mt_df.append(pd.DataFrame([[i, signal, score]], columns=['Ticker', 'Signal', 'Score']))
mt_df.index = ['NASDAQ', 'S&P500', 'DOW', 'KOSPI', 'KOSDAQ', 'BTC']
mt_msg = mt_df.sort_values(by=['Ticker'], axis=0).to_string()

us_score = str(round((mt_df.iloc[0]['Score'] + mt_df.iloc[1]['Score'] + mt_df.iloc[2]['Score'])/3, 1))
kr_score = str(round((mt_df.iloc[3]['Score'] + mt_df.iloc[4]['Score'])/2, 1))

bot.sendMessage(chat_id='*********', text=str(datetime.today().strftime('%Y-%m-%d %H:%M:%S')) + '\n' + '--------------------------' + '\n' + '| Market Timing information |'+ '\n' + 'US score :' + us_score + '\n' + 'KR score :' + kr_score + '\n' + '--------------------------' + '\n' + mt_msg + '\n' + '--------------------------')