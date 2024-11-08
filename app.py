import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import pandas as pd
import mplfinance as mpf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class StockApp:
    def __init__(self, root):
        """
        Initialize the StockApp class.

        Parameters:
        root (tk.Tk): The root window of the application.

        Attributes:
        root (tk.Tk): The root window of the application.
        symbol_var (tk.StringVar): Variable to store the stock symbol input.
        interval_var (tk.StringVar): Variable to store the selected interval.
        show_volume (tk.BooleanVar): Variable to track whether to show volume.
        show_rsi (tk.BooleanVar): Variable to track whether to show RSI.
        show_bbands (tk.BooleanVar): Variable to track whether to show Bollinger Bands.
        show_ma5 (tk.BooleanVar): Variable to track whether to show MA(5).
        show_ma20 (tk.BooleanVar): Variable to track whether to show MA(20).
        show_ma60 (tk.BooleanVar): Variable to track whether to show MA(60).
        show_ma200 (tk.BooleanVar): Variable to track whether to show MA(200).

        Returns:
        None
        """

        self.root = root
        self.root.title("Stock Candlestick Chart Viewer")

        # Handle window close event (clicking the X button)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.symbol_var = tk.StringVar()
        self.interval_var = tk.StringVar(value='1d')
        self.show_volume = tk.BooleanVar(value=True)
        self.show_rsi = tk.BooleanVar(value=False)
        self.show_bbands = tk.BooleanVar(value=False)
        self.show_ma5 = tk.BooleanVar(value=False)
        self.show_ma20 = tk.BooleanVar(value=False)
        self.show_ma60 = tk.BooleanVar(value=False)
        self.show_ma200 = tk.BooleanVar(value=False)

        self.create_widgets()

    def create_widgets(self):
        """
        Create and configure the widgets for the StockApp GUI.

        This function creates and packs various widgets such as labels, entry fields, buttons,
        checkboxes, and frames to control the stock data visualization.

        Parameters:
        None

        Returns:
        None
        """
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(control_frame, text="Symbol:").pack(
            side=tk.LEFT, padx=5, pady=5)
        symbol_entry = ttk.Entry(control_frame, textvariable=self.symbol_var)
        symbol_entry.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Button(control_frame, text="Load Data", command=self.load_data).pack(
            side=tk.LEFT, padx=5, pady=5)

        ttk.Label(control_frame, text="Interval:").pack(
            side=tk.LEFT, padx=5, pady=5)
        interval_combobox = ttk.Combobox(
            control_frame, textvariable=self.interval_var, values=['1d', '1wk', '1mo'])
        interval_combobox.pack(side=tk.LEFT, padx=5, pady=5)

        self.create_indicator_checkbuttons(control_frame)

        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def create_indicator_checkbuttons(self, frame):
        """
        Create and pack checkbuttons for selecting indicators to display on the stock chart.

        Parameters:
        frame (ttk.Frame): The frame in which to place the checkbuttons.

        Returns:
        None

        The function creates and packs checkbuttons for each indicator (Volume, RSI, Bollinger Bands,
        MA(5), MA(20), MA(60), MA(200)) using the provided frame. Each checkbutton is associated with
        a BooleanVar attribute of the StockApp class to track its state.
        """
        ttk.Checkbutton(frame, text="Volume", variable=self.show_volume).pack(
            side=tk.LEFT, padx=5, pady=5)
        ttk.Checkbutton(frame, text="RSI", variable=self.show_rsi).pack(
            side=tk.LEFT, padx=5, pady=5)
        ttk.Checkbutton(frame, text="Bollinger Bands", variable=self.show_bbands).pack(
            side=tk.LEFT, padx=5, pady=5)
        ttk.Checkbutton(frame, text="MA(5)", variable=self.show_ma5).pack(
            side=tk.LEFT, padx=5, pady=5)
        ttk.Checkbutton(frame, text="MA(20)", variable=self.show_ma20).pack(
            side=tk.LEFT, padx=5, pady=5)
        ttk.Checkbutton(frame, text="MA(60)", variable=self.show_ma60).pack(
            side=tk.LEFT, padx=5, pady=5)
        ttk.Checkbutton(frame, text="MA(200)", variable=self.show_ma200).pack(
            side=tk.LEFT, padx=5, pady=5)

    def load_data(self):
        """
        Load and process stock data for visualization.

        This function retrieves stock data from Yahoo Finance based on the user's input symbol and interval.
        It checks for input errors, handles exceptions, and calls the plot_data function to visualize the data.

        Parameters:
        self (StockApp): The instance of the StockApp class.

        Returns:
        None

        Raises:
        messagebox.showwarning: If the user does not enter a stock symbol.
        ValueError: If no data is found for the given symbol.
        messagebox.showerror: If an exception occurs during data retrieval or visualization.
        """
        symbol = self.symbol_var.get()
        interval = self.interval_var.get()

        if not symbol:
            messagebox.showwarning(
                "Input Error", "Please enter a stock symbol.")
            return

        try:
            data = yf.Ticker(symbol).history(period='1y', interval=interval)
            if data.empty:
                raise ValueError("No data found for this symbol.")
            self.plot_data(data)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def plot_data(self, data):
        """
        Plot stock data using Matplotlib Finance (mplfinance) library.

        This function clears the canvas frame, retrieves moving averages and additional plots (indicators),
        sets parameters for the plot, creates the plot, and displays it in a Tkinter canvas.

        Parameters:
        data (pandas.DataFrame): A DataFrame containing stock data with columns 'Open', 'High', 'Low', 'Close', and 'Volume'.

        Returns:
        None

        The function creates a plot using the provided data and the selected options (volume, indicators, moving averages).
        The plot is displayed in a Tkinter canvas within the canvas frame.
        """
        # Clear the canvas frame before plotting new data
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        # Get moving averages and additional plots (indicators)
        mav_values = self.get_mav()
        addplots = self.get_indicators(data)

        # Set parameters for the plot
        plot_params = {
            'data': data,
            'type': 'candle',
            'style': 'charles',
            'volume': self.show_volume.get(),
            'addplot': addplots,
            'returnfig': True,
            'figsize': (10, 6)
        }

        if mav_values:
            plot_params['mav'] = mav_values

        # Create the plot
        fig, axlist = mpf.plot(**plot_params)

        # Create a canvas to display the plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()

        # Pack the canvas widget to display it
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create and pack the toolbar
        toolbar = NavigationToolbar2Tk(canvas, self.canvas_frame)
        toolbar.update()
        toolbar.pack(side=tk.TOP, fill=tk.X)  # Pack the toolbar here

    def get_mav(self):
        """
        Retrieve the moving averages selected by the user.

        This function checks the state of the checkboxes for MA(5), MA(20), MA(60), and MA(200)
        and returns a list of the selected moving average periods. If no moving averages are selected,
        it returns None.

        Parameters:
        self (StockApp): The instance of the StockApp class.

        Returns:
        list or None: A list of selected moving average periods (e.g., [5, 20, 60, 200]) or None if no moving averages are selected.
        """
        mav_values = []
        if self.show_ma5.get():
            mav_values.append(5)
        if self.show_ma20.get():
            mav_values.append(20)
        if self.show_ma60.get():
            mav_values.append(60)
        if self.show_ma200.get():
            mav_values.append(200)
        return mav_values if mav_values else None

    def get_indicators(self, data):
        """
        Generate a list of additional plots (indicators) to be displayed on the stock chart.

        This function checks the state of the checkboxes for RSI and Bollinger Bands, calculates the
        respective indicators, and returns a list of addplot objects for mplfinance.plot().

        Parameters:
        data (pandas.DataFrame): A DataFrame containing stock data with columns 'Open', 'High', 'Low', 'Close', and 'Volume'.

        Returns:
        list: A list of addplot objects for mplfinance.plot(). Each addplot object represents an indicator to be displayed.
        """
        addplots = []
        if self.show_rsi.get():
            rsi = self.calculate_rsi(data['Close'])
            addplots.append(mpf.make_addplot(
                rsi, panel='lower', color='blue', ylabel='RSI'))
        if self.show_bbands.get():
            bbands = self.calculate_bbands(data)
            addplots += [
                mpf.make_addplot(bbands['Upper'], color='red'),
                mpf.make_addplot(bbands['Lower'], color='red')
            ]
        return addplots

    def calculate_rsi(self, series, period=14):
        """
        Calculate the Relative Strength Index (RSI) for a given price series.

        The RSI is a technical indicator used to measure the speed and strength of price movements.
        It is calculated using the average gain and loss over a specified period.

        Parameters:
        series (pandas.Series): A pandas Series containing the closing prices of a stock or other financial instrument.
        period (int, optional): The number of periods (days) to consider for calculating the RSI. Default is 14.

        Returns:
        pandas.Series: A pandas Series containing the calculated RSI values. The index of the Series is the same as the input series.
        """
        delta = series.diff(1)
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=period, min_periods=1).mean()
        avg_loss = loss.rolling(window=period, min_periods=1).mean()
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def calculate_bbands(self, data, window=20, no_of_std=2):
        """
        Calculate Bollinger Bands for a given price series.

        Bollinger Bands are a technical indicator used to identify overbought and oversold conditions.
        They consist of three lines: a simple moving average (middle band), an upper band, and a lower band.
        The bands are typically calculated using a moving average and standard deviation.

        Parameters:
        data (pandas.DataFrame): A DataFrame containing the closing prices of a stock or other financial instrument.
            The DataFrame should have a column named 'Close'.
        window (int, optional): The number of periods (days) to consider for calculating the moving average and standard deviation.
            Default is 20.
        no_of_std (int, optional): The number of standard deviations to use for calculating the upper and lower bands.
            Default is 2.

        Returns:
        pandas.DataFrame: A DataFrame containing the calculated Bollinger Bands. The DataFrame has two columns: 'Upper' and 'Lower'.
            The index of the DataFrame is the same as the input data.
        """
        rolling_mean = data['Close'].rolling(window).mean()
        rolling_std = data['Close'].rolling(window).std()
        upper_band = rolling_mean + (rolling_std * no_of_std)
        lower_band = rolling_mean - (rolling_std * no_of_std)
        return pd.DataFrame({'Upper': upper_band, 'Lower': lower_band}, index=data.index)

    def on_close(self):
        """
        Handle the window close event and properly close the application.

        This function is called when the user closes the window (by clicking the X button).
        It quits the Tkinter event loop, effectively terminating the application.

        Parameters:
        None

        Returns:
        None
        """
        self.root.quit()  # Properly close the application


if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()
