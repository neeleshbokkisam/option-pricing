# Standard library imports
import datetime

# Third party imports
import requests_cache
import yfinance as yf
import matplotlib.pyplot as plt
from pandas_datareader import data as wb

class Ticker:
    """Class for fetching data from Yahoo Finance."""
    
    @staticmethod
    def get_historical_data(ticker, start_date=None, end_date=None, cache_data=True, cache_days=1):
        """
        Fetches stock data from Yahoo Finance. Request is by default cached in an SQLite database for 1 day.
        
        Params:
        ticker: ticker symbol
        start_date: start date for getting historical data
        end_date: end date for getting historical data
        cache_data: flag for caching fetched data into SQLite database
        cache_days: number of days data will stay in cache 
        """
        try:
            # Fetch data using yfinance
            if start_date and end_date:
                data = yf.download(ticker, start=start_date, end=end_date)
            else:
                data = yf.download(ticker)
                
            if data.empty:
                raise ValueError(f"Failed to retrieve data for {ticker}.")

            return data
        except Exception as e:
            print(f"Error fetching data for ticker {ticker}: {e}")
            return None

    @staticmethod
    def get_columns(data):
        """
        Gets dataframe columns from previously fetched stock data.
        
        Params:
        data: dataframe representing fetched data
        """
        if data is None or data.empty:
            return None
        return list(data.columns)

    @staticmethod
    def get_last_price(data, column_name):
        """
        Returns last available price for specified column from already fetched data.
        
        Params:
        data: dataframe representing fetched data
        column_name: name of the column in dataframe
        """
        if data is None or column_name is None:
            return None
        if column_name not in Ticker.get_columns(data):
            print(f"Column {column_name} not found in data.")
            return None
        return data[column_name].iloc[-1]

    @staticmethod
    def plot_data(data, ticker, column_name, save_path):
        """
        Plots specified column values from dataframe and saves the plot to the specified path.

        Params:
        data: dataframe representing fetched data
        column_name: name of the column in dataframe
        save_path: path where the plot image will be saved
        """
        try:
            if data is None:
                return
            plt.figure(figsize=(10, 6))
            data[column_name].plot()
            plt.ylabel(f'{column_name}')
            plt.xlabel('Date')
            plt.title(f'Historical data for {ticker} - {column_name}')
            plt.legend(loc='best')
            plt.savefig(save_path)  # Save the plot instead of showing it
            plt.close()  # Close the plot to free up memory
        except Exception as e:
            print(e)
            return

