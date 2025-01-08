import streamlit as st
import plotly.graph_objs as go
import yfinance as yf  # Pastikan yfinance diinstal

# Fungsi untuk mendapatkan data ticker
def get_ticker_data(ticker_symbol, data_period, data_interval):
    try:
        ticker_data = yf.download(tickers=ticker_symbol, period=data_period, interval=data_interval)
        if ticker_data.empty:
            st.error('Could not find the ticker data. Please modify the ticker symbol or reduce the period value.')
            return None
        # Format tanggal di indeks untuk tampilan yang lebih baik
        ticker_data.index = ticker_data.index.strftime("%d-%m-%Y %H:%M")
        return ticker_data
    except Exception as e:
        st.error(f"An error occurred while fetching the data: {e}")
        return None

# Fungsi untuk membuat grafik candlestick
def plot_candle_chart(ticker_data):
    try:
        candle_fig = go.Figure()
        candle_fig.add_trace(
            go.Candlestick(
                x=ticker_data.index,
                open=ticker_data['Open'],
                close=ticker_data['Close'],
                low=ticker_data['Low'],
                high=ticker_data['High'],
                name='Market Data'
            )
        )
        candle_fig.update_layout(
            title="Candlestick Chart",
            xaxis_title="Date",
            yaxis_title="Price",
            height=800
        )
        st.plotly_chart(candle_fig)
    except Exception as e:
        st.error(f"An error occurred while plotting the chart: {e}")

# Program utama
if __name__ == '__main__':
    # Sidebar untuk input pengguna
    ticker_symbol = st.sidebar.text_input("Enter the stock symbol:", 'MSFT')
    data_period = st.sidebar.text_input('Enter the period (e.g., 10d, 1mo):', '10d')
    data_interval = st.sidebar.radio('Select the interval:', ['15m', '30m', '1h', '1d', '5d'])

    st.header(f"Stock Data for: {ticker_symbol}")

    # Ambil data ticker menggunakan fungsi yang sudah diperbaiki
    ticker_data = get_ticker_data(ticker_symbol, data_period, data_interval)
    
    # Jika data tersedia, tampilkan grafik candlestick
    if ticker_data is not None and not ticker_data.empty:
        plot_candle_chart(ticker_data)
