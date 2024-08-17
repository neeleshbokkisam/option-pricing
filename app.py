from flask import Flask, render_template, request
from datetime import datetime, timedelta
from models.BlackScholesModel import BlackScholesModel
from models.MonteCarloPricing import MonteCarloPricing
from models.BinomialTreeModel import BinomialTreeModel
from models.ticker import Ticker
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/black_scholes', methods=['GET', 'POST'])
def black_scholes():
    if request.method == 'POST':
        # Get form data
        ticker = request.form['ticker']
        strike_price = float(request.form['strike_price'])
        risk_free_rate = float(request.form['risk_free_rate']) / 100
        sigma = float(request.form['sigma']) / 100
        exercise_date = datetime.strptime(request.form['exercise_date'], '%Y-%m-%d')
        
        # Get historical data for the ticker
        data = Ticker.get_historical_data(ticker)
        spot_price = Ticker.get_last_price(data, 'Adj Close')
        days_to_maturity = (exercise_date.date() - datetime.now().date()).days

        # Check if data is valid
        if spot_price is None:
            return render_template('error.html', message=f"Failed to retrieve data for {ticker}. Please check the ticker symbol or try again later.")

        # Calculate option prices using Black-Scholes model
        BSM = BlackScholesModel(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma)
        call_option_price = BSM._calculate_call_option_price()
        put_option_price = BSM._calculate_put_option_price()

        # Plotting historical data
        plot_file_path = 'static/historical_data_plot.png'
        Ticker.plot_data(data, ticker, 'Adj Close', save_path=plot_file_path)

        return render_template('black_scholes_result.html', 
                               call_option_price=call_option_price, 
                               put_option_price=put_option_price, 
                               plot_url=plot_file_path)

    default_exercise_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
    return render_template('black_scholes_form.html', default_exercise_date=default_exercise_date, datetime=datetime, timedelta=timedelta)


@app.route('/monte_carlo', methods=['GET', 'POST'])
def monte_carlo():
    if request.method == 'POST':
        # Get form data
        ticker = request.form['ticker']
        strike_price = float(request.form['strike_price'])
        risk_free_rate = float(request.form['risk_free_rate']) / 100
        sigma = float(request.form['sigma']) / 100
        exercise_date = datetime.strptime(request.form['exercise_date'], '%Y-%m-%d')
        number_of_simulations = int(request.form['num_simulations'])
        num_of_movements = int(request.form['num_of_movements'])

        # Get historical data for the ticker
        data = Ticker.get_historical_data(ticker)
        spot_price = Ticker.get_last_price(data, 'Adj Close')
        days_to_maturity = (exercise_date.date() - datetime.now().date()).days

        # Simulate and calculate option prices
        MC = MonteCarloPricing(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_simulations)
        MC.simulate_prices()
        call_option_price = MC._calculate_call_option_price()
        put_option_price = MC._calculate_put_option_price()

        # Save plots to static folder
        simulation_plot_file_path = os.path.join('static', 'monte_carlo_simulation_plot.png')
        historical_plot_file_path = os.path.join('static', 'monte_carlo_historical_plot.png')
        MC.plot_simulation_results(num_of_movements, simulation_plot_file_path, historical_plot_file_path, historical_data=data, ticker=ticker)

        return render_template('monte_carlo_result.html', 
                               call_option_price=call_option_price, 
                               put_option_price=put_option_price, 
                               simulation_plot_url=simulation_plot_file_path,
                               historical_plot_url=historical_plot_file_path)

    return render_template('monte_carlo_form.html')


@app.route('/binomial_tree', methods=['GET', 'POST'])
def binomial_tree():
    if request.method == 'POST':
        # Get form data
        ticker = request.form['ticker']
        strike_price = float(request.form['strike_price'])
        risk_free_rate = float(request.form['risk_free_rate']) / 100
        sigma = float(request.form['sigma']) / 100
        exercise_date = datetime.strptime(request.form['exercise_date'], '%Y-%m-%d')
        number_of_time_steps = int(request.form['number_of_time_steps'])

        # Get historical data for the ticker
        data = Ticker.get_historical_data(ticker)
        spot_price = Ticker.get_last_price(data, 'Adj Close')
        days_to_maturity = (exercise_date.date() - datetime.now().date()).days

        # Check if data is valid
        if spot_price is None:
            return render_template('error.html', message=f"Failed to retrieve data for {ticker}. Please check the ticker symbol or try again later.")

        # Calculate option prices using Binomial-Tree model
        BOPM = BinomialTreeModel(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_time_steps)
        call_option_price = BOPM.calculate_option_price('Call Option')
        put_option_price = BOPM.calculate_option_price('Put Option')

        # Plot historical data
        plot_file_path = 'static/binomial_tree_plot.png'
        Ticker.plot_data(data, ticker, 'Adj Close', save_path=plot_file_path)

        # Render result template with the calculated option prices and the plot
        return render_template('binomial_tree_result.html', 
                               call_option_price=call_option_price, 
                               put_option_price=put_option_price, 
                               plot_url=plot_file_path)

    default_exercise_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
    return render_template('binomial_tree_form.html', default_exercise_date=default_exercise_date, datetime=datetime, timedelta=timedelta)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

