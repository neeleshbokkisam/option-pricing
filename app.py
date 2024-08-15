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

        # Displaying call/put option price and plot
        Ticker.plot_data(data, ticker, 'Adj Close')  # Save the plot image to be rendered on the result page
        plot_file_path = 'static/plot.png'  # Assuming the plot is saved here

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

        # Debugging statements to check form inputs
        print(f"ticker: {ticker}")
        print(f"strike_price: {strike_price}")
        print(f"risk_free_rate: {risk_free_rate}")
        print(f"sigma: {sigma}")
        print(f"exercise_date: {exercise_date}")
        print(f"number_of_simulations: {number_of_simulations}")
        print(f"num_of_movements: {num_of_movements}")

        # Get historical data for the ticker
        data = Ticker.get_historical_data(ticker)
        print(f"Historical data for {ticker}: {data}")
        spot_price = Ticker.get_last_price(data, 'Adj Close')
        days_to_maturity = (exercise_date.date() - datetime.now().date()).days

        # Debugging statements to check processed values
        print(f"spot_price: {spot_price}")
        print(f"days_to_maturity: {days_to_maturity}")

        # Simulate and calculate option prices
        MC = MonteCarloPricing(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_simulations)
        MC.simulate_prices()
        call_option_price = MC._calculate_call_option_price()
        put_option_price = MC._calculate_put_option_price()

        # Debugging statements to check calculated prices
        print(f"call_option_price: {call_option_price}")
        print(f"put_option_price: {put_option_price}")

        # Save plot to static folder
        plot_file_path = os.path.join('static', 'monte_carlo_plot.png')
        MC.plot_simulation_results(num_of_movements, plot_file_path)

        return render_template('monte_carlo_result.html', call_option_price=call_option_price, put_option_price=put_option_price, plot_url=plot_file_path)

    return render_template('monte_carlo_form.html')




@app.route('/binomial', methods=['GET', 'POST'])
def binomial():
    if request.method == 'POST':
        # Get form data
        ticker = request.form['ticker']
        strike_price = float(request.form['strike_price'])
        risk_free_rate = float(request.form['risk_free_rate']) / 100
        sigma = float(request.form['sigma']) / 100
        exercise_date = datetime.strptime(request.form['exercise_date'], '%Y-%m-%d')
        number_of_time_steps = int(request.form['num_time_steps'])

        # Get historical data for the ticker
        data = Ticker.get_historical_data(ticker)
        spot_price = Ticker.get_last_price(data, 'Adj Close')
        days_to_maturity = (exercise_date - datetime.now().date()).days

        # Calculate option prices
        BOPM = BinomialTreeModel(spot_price, strike_price, days_to_maturity, risk_free_rate, sigma, number_of_time_steps)
        call_option_price = BOPM.calculate_option_price('call')
        put_option_price = BOPM.calculate_option_price('put')

        return render_template('result.html', call_option_price=call_option_price, put_option_price=put_option_price)

    return render_template('binomial_form.html')

if __name__ == '__main__':
    app.run(debug=True)
