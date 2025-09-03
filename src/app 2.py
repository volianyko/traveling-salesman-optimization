from flask import Flask, render_template, jsonify, request
import json

#import python files with algorithms
import sys
sys.path.append("algorithms")  

from algorithms.common import *
from algorithms.aco import *
from algorithms.sa import *
from algorithms.held_karp import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('start.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/calculate_outputs', methods=['POST'])
def calculate_outputs_api():
    #get the data in the request
    data = request.get_json()
    #match the fields
    coordinates = data['coordinates']
    aco_a = data['aco_a']
    aco_b = data['aco_b']
    aco_Q = data['aco_Q']
    aco_er = data['aco_er']
    aco_ants = data['aco_ants']
    aco_iter = data['aco_iter']
    aco_shake = data['aco_shake']
    sa_a = data['sa_a']
    sa_T = data['sa_T']
    sa_iter = data['sa_iter']
    #add the distance matrix
    n, dist = calculate_distance_matrix(coordinates)
    #create a tsp input object
    tsp_input = TSP_input(n, dist, coordinates)
    #create aco parameters object
    aco_input = ACO_parameters(aco_a, aco_b, aco_Q, aco_er, aco_ants, aco_iter, aco_shake)
    #create sa parameters object
    sa_input = SA_parameters(sa_a, sa_T, sa_iter)

    #pass the inputs to corresponding functions
    hk_output = held_karp(tsp_input)
    aco_it_found, aco_output = solve_aco(tsp_input, aco_input)
    sa_it_found, sa_output = solve_sa(tsp_input, sa_input)

    #jsonify the held-karp output to be able to return it
    hk_output = json.dumps(vars(hk_output))

    #jsonify iterations of aco output
    for i in range(len(aco_output)):
        aco_output[i] = json.dumps(aco_output[i].__dict__)
    #jsonify iterarations of sa output
    for i in range(len(sa_output)):
        sa_output[i] = json.dumps(sa_output[i].__dict__)
    
    #return a json with all outputs
    return jsonify({
        'hk_output': hk_output,
        'aco_it_found': aco_it_found,
        'aco_output': aco_output,
        'sa_it_found': sa_it_found,
        'sa_output': sa_output
    })

if __name__ == "__main__":
    app.run(debug=True)