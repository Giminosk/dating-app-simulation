from flask import Flask, request, jsonify, render_template, send_from_directory, make_response
from simulation import Simulation


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/plots/<filename>')
def send_plot(filename):
    response = make_response(send_from_directory('plots', filename))
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.route('/run_simulation', methods=['POST'])
def run_simulation():
    data = request.json
    men_users = int(data.get('men_users', 0))
    men_swipes = int(data.get('men_swipes', 0))
    men_formula = data.get('men_formula', '')
    
    women_users = int(data.get('women_users', 0))
    women_swipes = int(data.get('women_swipes', 0))
    women_formula = data.get('women_formula', '')
    
    simulation = Simulation(
        num_men=men_users,
        num_women=women_users,
        num_swipes_per_day_men=men_swipes,
        num_swipes_per_day_women=women_swipes,
        men_formula=men_formula,
        women_formula=women_formula
    )
    
    simulation.simulate()
    stats = simulation.get_stats()
    # print(stats)

    results = {
        'input_params': data,
        'stats': stats, 
        'output': 'Simulation results would go here'
    }
    return jsonify(results)
