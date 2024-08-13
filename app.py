from flask import Flask, render_template, request
from models.BlackScholesModel import BlackScholesModel

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/black_scholes', methods=['GET', 'POST'])
def black_scholes():
    if request.method == 'POST':
        # Get form data
        S = float(request.form['S'])
        K = float(request.form['K'])
        T = float(request.form['T'])
        r = float(request.form['r'])
        sigma = float(request.form['sigma'])
        option_type = request.form['option_type']
        
        # Calculate option price using Black-Scholes Model
        model = BlackScholesModel(S, K, T, r, sigma)
        price = model.calculate_option_price(option_type=option_type)

        return render_template('black_scholes_result.html', price=price)

    return render_template('black_scholes_form.html')


# Routes for other models (Monte Carlo, Binomial Tree)
@app.route('/monte_carlo', methods=['GET', 'POST'])
def monte_carlo():
    return "<h2>Monte Carlo Simulation - Coming Soon</h2>"

@app.route('/binomial_tree', methods=['GET', 'POST'])
def binomial_tree():
    return "<h2>Binomial Tree Model - Coming Soon</h2>"

if __name__ == '__main__':
    app.run(debug=True)
