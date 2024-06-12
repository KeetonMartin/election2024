import numpy as np
import pandas as pd

def simulate_election(pivot_avg_data, electoral_votes, num_simulations=1000, stddev_national=4.0, stddev_state=3.0):
    results = {'Donald Trump': 0, 'Joe Biden': 0}
    simulation_details = []

    for _ in range(num_simulations):
        national_error = np.random.normal(0, stddev_national)
        simulated_data = pivot_avg_data.copy()
        simulated_data['state_error'] = np.random.normal(0, stddev_state, simulated_data.shape[0])
        simulated_data['simulated_diff'] = simulated_data['differential'] + national_error + simulated_data['state_error']
        simulated_data['simulated_winner'] = simulated_data['simulated_diff'].apply(lambda x: 'Donald Trump' if x > 0 else 'Joe Biden')
        
        state_winners = simulated_data[['simulated_winner']].merge(pd.DataFrame(electoral_votes.items(), columns=['state', 'electoral_votes']), left_index=True, right_on='state')
        electoral_counts = state_winners.groupby('simulated_winner')['electoral_votes'].sum()
        
        simulation_details.append(electoral_counts)
        
        if 'Donald Trump' in electoral_counts and electoral_counts['Donald Trump'] >= 270:
            results['Donald Trump'] += 1
        if 'Joe Biden' in electoral_counts and electoral_counts['Joe Biden'] >= 270:
            results['Joe Biden'] += 1
    
    simulation_summary = pd.DataFrame(simulation_details).fillna(0).mean()
    win_probabilities = {candidate: results[candidate] / num_simulations for candidate in results}
    return win_probabilities, simulation_summary
