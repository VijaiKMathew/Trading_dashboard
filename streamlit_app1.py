import yfinance as yf
import streamlit as st
import datetime 
# import talib 
import pandas_ta as ta1
import ta
import pandas as pd
import requests
yf.pdr_override()

st.write("""
# Technical Analysis Web Application
Shown below are the **Moving Average Crossovers**, **Bollinger Bands**, **MACD's**, **Commodity Channel Indexes**, and **Relative Strength Indexes** of any stock!
""")

st.sidebar.header('User Input Parameters')

today = datetime.date.today()
def user_input_features():
    ticker = st.sidebar.text_input("Ticker", 'AAPL')
    start_date = st.sidebar.text_input("Start Date", '2019-01-01')
    end_date = st.sidebar.text_input("End Date", f'{today}')
    return ticker, start_date, end_date

symbol, start, end = user_input_features()

def get_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)
    result = requests.get(url).json()
    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']
company_name = get_symbol(symbol.upper())

start = pd.to_datetime(start)
end = pd.to_datetime(end)

# Read data 
data = yf.download(symbol,start,end)

# Adjusted Close Price
st.header(f"Adjusted Close Price\n {company_name}")
st.line_chart(data['Adj Close'])

# ## SMA and EMA
#Simple Moving Average
data['SMA'] = ta1.sma(data['Adj Close'], timeperiod = 20)

# Exponential Moving Average
data['EMA'] = ta1.ema(data['Adj Close'], timeperiod = 20)

# Plot
st.header(f"Simple Moving Average vs. Exponential Moving Average\n {company_name}")
st.line_chart(data[['Adj Close','SMA','EMA']])

# Bollinger Bands
data[['lower_band','middle_band','upper_band']] = ta1.bbands(data['Adj Close'], timeperiod =20).iloc[:, 0:3]

# Plot
st.header(f"Bollinger Bands\n {company_name}")
st.line_chart(data[['Adj Close','upper_band','middle_band','lower_band']])

# ## MACD (Moving Average Convergence Divergence)
# MACD
data[['macd','macdhist','macdsignal']]= ta1.macd(data['Adj Close'], fastperiod=12, slowperiod=26, signalperiod=9).iloc[:, 0:3]

# Plot
st.header(f"Moving Average Convergence Divergence\n {company_name}")
st.line_chart(data[['macd','macdsignal']])

## CCI (Commodity Channel Index)
# CCI
cci = ta.trend.cci(data['High'], data['Low'], data['Close'], window=31, constant=0.015)

# Plot
st.header(f"Commodity Channel Index\n {company_name}")
st.line_chart(cci)

# ## RSI (Relative Strength Index)
# RSI
data['RSI'] = ta1.rsi(data['Adj Close'], timeperiod=14)

# Plot
st.header(f"Relative Strength Index\n {company_name}")
st.line_chart(data['RSI'])

# ## OBV (On Balance Volume)
# OBV
data['OBV'] = ta1.obv(data['Adj Close'], data['Volume'])/10**6

# Plot
st.header(f"On Balance Volume\n {company_name}")
st.line_chart(data['OBV'])