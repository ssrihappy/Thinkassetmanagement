import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import telegram

token = '텔레그램 토큰을 적어주세요'
bot = telegram.Bot(token=token)
id = bot.getUpdates()[-1].message.chat.id

canary = ['VWO', 'BND']
attack = ['SPY', 'IWN', 'QQQ', 'VGK', 'EWJ', 'VWO', 'VNQ', 'GSG', 'GLD', 'TLT', 'HYG', 'LQD']
defense = ['SHV', 'IEF', 'UST']

def cls_prices(ticker, mvday, day):
    now = datetime.today().strftime('%Y-%m-%d')
    start = (datetime.today() - relativedelta(years=1, months=1)).strftime('%Y-%m-%d')
    close = yf.download(ticker, start=start, end=now)
    sma = close.Close.rolling(window=mvday).mean()[-1]
    price = close.Close[-day]
    return sma, price

canary_df = pd.DataFrame(columns = ['Ticker(canary)', 'Score', 'Score(-1 mo)'])
attack_df = pd.DataFrame(columns = ['Ticker', 'Score', 'Score(-1 mo)'])
defense_df = pd.DataFrame(columns = ['Ticker', 'Score', 'Score(-1 mo)'])

for j in canary:
    p_0 = cls_prices(j, 1, 1)[1]
    p_20 = cls_prices(j, 1, 21)[1]
    p_40 = cls_prices(j, 1, 41)[1]
    p_60 = cls_prices(j, 1, 61)[1]
    p_80 = cls_prices(j, 1, 81)[1]
    p_120 = cls_prices(j, 1, 121)[1]
    p_140 = cls_prices(j, 1, 141)[1]
    p_240 = cls_prices(j, 1, 241)[1]
    p_260 = cls_prices(j, 1, 261)[1]

    canary_score = round(12*(float(p_0/p_20)-1)+4*(float(p_0/p_60)-1)+2*(float(p_0/p_120)-1)+1*(float(p_0/p_240)-1), 4)*100
    canary_score2 = round(12*(float(p_20/p_40)-1)+4*(float(p_20/p_80)-1)+2*(float(p_20/p_140)-1)+1*(float(p_20/p_260)-1), 4)*100
    canary_df = canary_df.append(pd.DataFrame([[j, canary_score, canary_score2]], columns=['Ticker(canary)', 'Score', 'Score(-1 mo)']))
    canary_msg = canary_df.sort_values(by=['Score'], axis=0, ascending=False).to_string(index=False)

for i in attack:
    p_0 = cls_prices(i, 1, 1)[1]
    p_20 = cls_prices(i, 1, 21)[1]
    p_40 = cls_prices(i, 1, 41)[1]
    p_60 = cls_prices(i, 1, 61)[1]
    p_80 = cls_prices(i, 1, 81)[1]
    p_120 = cls_prices(i, 1, 121)[1]
    p_140 = cls_prices(i, 1, 141)[1]
    p_240 = cls_prices(i, 1, 241)[1]
    p_260 = cls_prices(i, 1, 261)[1]

    attack_score = round(12*(float(p_0/p_20)-1)+4*(float(p_0/p_60)-1)+2*(float(p_0/p_120)-1)+1*(float(p_0/p_240)-1), 4)*100
    attack_score2 = round(12*(float(p_20/p_40)-1)+4*(float(p_20/p_80)-1)+2*(float(p_20/p_140)-1)+1*(float(p_20/p_260)-1), 4)*100
    attack_df = attack_df.append(pd.DataFrame([[i, attack_score, attack_score2]], columns=['Ticker', 'Score', 'Score(-1 mo)']))
    msg_att = attack_df.sort_values(by=['Score'], axis=0, ascending=False).to_string(index=False)

for l in defense:
    p_0 = cls_prices(l, 1, 1)[1]
    p_20 = cls_prices(l, 1, 21)[1]
    p_40 = cls_prices(l, 1, 41)[1]
    p_60 = cls_prices(l, 1, 61)[1]
    p_80 = cls_prices(l, 1, 81)[1]
    p_120 = cls_prices(l, 1, 121)[1]
    p_140 = cls_prices(l, 1, 141)[1]
    p_240 = cls_prices(l, 1, 241)[1]
    p_260 = cls_prices(l, 1, 261)[1]

    defense_score = round(12*(float(p_0/p_20)-1)+4*(float(p_0/p_60)-1)+2*(float(p_0/p_120)-1)+1*(float(p_0/p_240)-1), 4)*100
    defense_score2 = round(12*(float(p_20/p_40)-1)+4*(float(p_20/p_80)-1)+2*(float(p_20/p_140)-1)+1*(float(p_20/p_260)-1), 4)*100
    defense_df = defense_df.append(pd.DataFrame([[l, defense_score, defense_score2]], columns=['Ticker', 'Score', 'Score(-1 mo)']))
    msg_def = defense_df.sort_values(by=['Score'], axis=0, ascending=False).to_string(index=False)

if canary_df.iloc[0]['Score'] and canary_df.iloc[1]['Score'] > 0:
    bot.sendMessage(chat_id=id, text=str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))+ '\n' + '\n' + canary_msg + '\n' + '---------------------------------------' + '\n' + 'Buy top 2 stocks in attack, 50%/50%' + '\n' + '---------------------------------------'+ '\n'+'\n' + msg_att)

elif canary_df.iloc[0]['Score'] or canary_df.iloc[1]['Score'] < 0:
    bot.sendMessage(chat_id=id, text=str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))+ '\n' + '\n' + canary_msg + '\n' + '---------------------------------------' + '\n' + 'Buy the top 1 stock in defense, 100%' +'\n' + '---------------------------------------'+ '\n'+'\n' + msg_def)

else:
    bot.sendMessage(chat_id=id, text=str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))+ '\n' + 'Holding')