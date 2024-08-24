import numpy as np
import pandas as pd
import json
from datetime import datetime

def simulate_election(pivot_avg_data, electoral_votes, num_simulations=1000, stddev_national=4.0, stddev_state=3.0):
    results = {'Donald Trump': 0, 'Kamala Harris': 0}
    simulation_details = []

    for _ in range(num_simulations):
        national_error = np.random.normal(0, stddev_national)
        simulated_data = pivot_avg_data.copy()
        simulated_data['state_error'] = np.random.normal(0, stddev_state, simulated_data.shape[0])
        simulated_data['simulated_diff'] = simulated_data['differential'] + national_error + simulated_data['state_error']
        simulated_data['simulated_winner'] = simulated_data['simulated_diff'].apply(lambda x: 'Donald Trump' if x > 0 else 'Kamala Harris')
        
        state_winners = simulated_data[['simulated_winner']].merge(pd.DataFrame(electoral_votes.items(), columns=['state', 'electoral_votes']), left_index=True, right_on='state')
        electoral_counts = state_winners.groupby('simulated_winner')['electoral_votes'].sum()
        
        simulation_details.append(electoral_counts)
        
        if 'Donald Trump' in electoral_counts and electoral_counts['Donald Trump'] >= 270:
            results['Donald Trump'] += 1
        if 'Kamala Harris' in electoral_counts and electoral_counts['Kamala Harris'] >= 270:
            results['Kamala Harris'] += 1
    
    simulation_summary = pd.DataFrame(simulation_details).fillna(0).mean()
    win_probabilities = {candidate: results[candidate] / num_simulations for candidate in results}
    
    # Append results to JSON file
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result_entry = {
        "timestamp": timestamp,
        "win_probabilities": win_probabilities,
        "simulation_summary": simulation_summary.to_dict()
    }
    
    try:
        with open("simulation_results.json", "r+") as f:
            data = json.load(f)
            data.append(result_entry)
            f.seek(0)
            json.dump(data, f, indent=2)
    except FileNotFoundError:
        with open("simulation_results.json", "w") as f:
            json.dump([result_entry], f, indent=2)
    
    return win_probabilities, simulation_summary