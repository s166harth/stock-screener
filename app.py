import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
from keras.models import load_model
import datetime
import streamlit as st
def rsi(df, periods = 14, ema = True):
   
    close_delta = df['Close'].diff()

   
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    if ema == True:
	    
        ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
        ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    else:
       
        ma_up = up.rolling(window = periods, adjust=False).mean()
        ma_down = down.rolling(window = periods, adjust=False).mean()
        
    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))
    return rsi
def get_sma(prices, rate):
    return prices.rolling(rate).mean()

def get_bollinger_bands(prices, rate=20):
    sma = get_sma(prices, rate)
    std = prices.rolling(rate).std()
    bollinger_up = sma + std * 2 # Calculate top band
    bollinger_down = sma - std * 2 # Calculate bottom band
    return bollinger_up, bollinger_down

def main():
    st.title('Ticker')

    start = st.date_input('Start date')
    end = st.date_input('End date')
    ticker = st.text_input('Enter Ticker','AAPL')

    df = data.DataReader(ticker,'yahoo',start,end)




    st.subheader('Data')
    st.write(df.describe())
    #df=df.drop(['Date','Low','High','Open','Adj Close','Volume'],axis=1)
    st.subheader('Closing vs. time')
    fig=plt.figure(figsize=(12,6))
    plt.plot(df.Close)
    st.pyplot(fig)

    st.subheader('100-day Moving Average')
    ma100 = df.Close.rolling(100).mean()
    ma200 = df.Close.rolling(200).mean()
    fig100=plt.figure(figsize=(12,6))
    plt.plot(df.Close)
    plt.plot(ma100,'r')
    #plt.plot(ma200,'green')
    st.pyplot(fig100)

    st.subheader('100&200-day Moving Average')
    ma100 = df.Close.rolling(100).mean()
    ma200 = df.Close.rolling(200).mean()
    fig200=plt.figure(figsize=(12,6))
    plt.plot(df.Close)
    plt.plot(ma100,'r')
    plt.plot(ma200,'green')
    st.pyplot(fig200)


    # data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
    # data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])


    # from sklearn.preprocessing import MinMaxScaler
    # scaler=MinMaxScaler(feature_range=(0,1))
    # data_training_array = scaler.fit_transform(data_training)



    # model=load_model('stockmodel.h5')
    # past_100_days = data_training.tail(100)
    # final_df = past_100_days.append(data_testing,ignore_index=True)
    # input_data = scaler.fit_transform(final_df)
    # x_test=[]
    # y_test=[]
    # predictions=[]
    # for i in range(100,input_data.shape[0]):
    #     predictions.append(input_data[i-100:i])
    #     x_test.append(input_data[i-100:i])
    #     y_test.append(input_data[i,0])
        
    # x_test,y_test=np.array(x_test),np.array(y_test)
    # y_predicted=model.predict(x_test)
    # scaler=scaler.scale_
    # scale_factor=1/scaler[0]

    # y_predicted=y_predicted*scale_factor
    # y_test=y_test*scale_factor

    # st.subheader('Prediction vs. original')
    # figp=plt.figure(figsize=(20,15))
    # plt.plot(y_test,'b',label='Original Price')
    # plt.plot(y_predicted,'r',label='Predition')
    # plt.xlabel('Time')
    # plt.ylabel('Price')
    # plt.legend()
    # st.pyplot(figp)



    st.subheader('RSI(Relative strength index)')
    rsi_ = rsi(df,14,True)
    figrsi = plt.figure(figsize=(12,6))
    plt.plot(rsi_)

    st.pyplot(figrsi)



        
    df=df.drop(['Low','High','Open','Adj Close','Volume'],axis=1)
    bollinger_up, bollinger_down = get_bollinger_bands(df)

    st.subheader('Bollinger Bands')

    figbo = plt.figure(figsize=(12,6))
    plt.xlabel('Days')
    plt.ylabel('Closing Prices')
    plt.plot(df, label='Closing Prices')
    plt.plot(bollinger_up, label='Bollinger Up', c='g')
    plt.plot(bollinger_down, label='Bollinger Down', c='r')
    plt.legend()
    st.pyplot(figbo)



if __name__=='__main__':
    main()