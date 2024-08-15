from models.ticker import Ticker

# Test the get_historical_data method
ticker_symbol = "AAPL"  # Use a known valid ticker symbol
start_date = "2023-01-01"  # Optional: Specify a start date
end_date = "2023-12-31"    # Optional: Specify an end date

data = Ticker.get_historical_data(ticker_symbol, start_date=start_date, end_date=end_date)

if data is not None:
    print(f"Historical data for {ticker_symbol}:")
    print(data.head())  # Print the first few rows of data
else:
    print(f"Failed to retrieve data for {ticker_symbol}.")
