
# Stock Candlestick Chart Viewer

A simple Tkinter-based stock chart viewer that allows you to visualize candlestick charts with various technical indicators, including Moving Averages (MA), Bollinger Bands, and Relative Strength Index (RSI). The data is fetched from Yahoo Finance using the `yfinance` library.

## Features
- Display stock candlestick charts.
- View additional technical indicators: 
  - Volume
  - RSI (Relative Strength Index)
  - Bollinger Bands
  - Moving Averages (MA) for 5, 20, 60, and 200 periods.
- User-friendly interface to input stock symbols and intervals (1 day, 1 week, 1 month).
- Interactive chart navigation using the `mplfinance` library.

## Requirements
- Python 3.x
- `tkinter` (usually included with Python)
- `yfinance`  
- `mplfinance`  
- `matplotlib`  
- `pandas`  

You can install the required dependencies using `pip`:

```bash
pip install yfinance mplfinance matplotlib pandas
```

## Usage
1. Run the script to open the Stock Candlestick Chart Viewer.
2. Enter the stock symbol (e.g., AAPL, TSLA) and select the desired interval (1d, 1wk, 1mo).
3. Optionally enable/disable technical indicators like RSI, Bollinger Bands, and Moving Averages.
4. Click "Load Data" to fetch and visualize the stock data.

## License
This project is licensed under the MIT License.
