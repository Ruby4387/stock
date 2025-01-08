import streamlit as st
import plotly.graph_objs as go
import yfinance as yf  # Ensure yfinance is installed

def get_ticker_data(ticker_symbol, data_period, data_interval):
    try:
        ticker_data = yf.download(tickers=ticker_symbol, period=data_period, interval=data_interval)
        if ticker_data.empty:
            return None
        return ticker_data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

def plot_candle_chart(ticker_data):
    required_columns = ['Open', 'Close', 'High', 'Low']
    if not all(col in ticker_data.columns for col in required_columns):
        st.error("Data is missing required columns for plotting candlestick chart.")
        return
    
    candle_fig = go.Figure()
    candle_fig.add_trace(
        go.Candlestick(
            x=ticker_data.index,
            open=ticker_data['Open'],
            high=ticker_data['High'],
            low=ticker_data['Low'],
            close=ticker_data['Close'],
            name="Market Data"
        )
    )
    candle_fig.update_layout(
        title="Candlestick Chart",
        xaxis_title="Time",
        yaxis_title="Price",
        height=800
    )
    st.plotly_chart(candle_fig)

# if __name__ == '__main__':
st.sidebar.title("Stock Market Dashboard")
ticker_symbol = st.sidebar.text_input("Enter stock symbol (e.g., MSFT, AAPL):", 'MSFT')
data_period = st.sidebar.text_input("Enter period (e.g., 1d, 5d, 1mo):", '1d')
data_interval = st.sidebar.radio("Select interval:", ['15m', '30m', '1h', '1d', '5d'])

st.title(f"Stock Data for {ticker_symbol}")

ticker_data = get_ticker_data(ticker_symbol, data_period, data_interval)
if ticker_data is None or ticker_data.empty:
    st.error("No data available for the selected ticker and parameters.")
else:
    plot_candle_chart(ticker_data)