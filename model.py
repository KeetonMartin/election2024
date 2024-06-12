import numpy as np
import pandas as pd
from data_processing import load_poll_data, process_poll_data, calculate_differential_and_winner, add_electoral_votes, summarize_electoral_votes
from assumptions import apply_polling_assumptions
from electoral_votes import electoral_votes
from state_abbreviations import state_abbreviations
from utils import plot_electoral_college, plot_choropleth

def simulate_election(pivot_avg_data, electoral_votes, num_simulations=1000, stddev=5.0):
    results = {'Donald Trump': 0, 'Joe Biden': 0}
    
    for _ in range(num_simulations):
        simulated_data = pivot_avg_data.copy()
        simulated_data['simulated_diff'] = np.random.normal(simulated_data['differential'], stddev)
        simulated_data['simulated_winner'] = simulated_data['simulated_diff'].apply(lambda x: 'Donald Trump' if x > 0 else 'Joe Biden')
        
        state_winners = simulated_data[['simulated_winner']].merge(pd.DataFrame(electoral_votes.items(), columns=['state', 'electoral_votes']), left_index=True, right_on='state')
        electoral_counts = state_winners.groupby('simulated_winner')['electoral_votes'].sum()
        
        if 'Donald Trump' in electoral_counts and electoral_counts['Donald Trump'] >= 270:
            results['Donald Trump'] += 1
        if 'Joe Biden' in electoral_counts and electoral_counts['Joe Biden'] >= 270:
            results['Joe Biden'] += 1
    
    return results

file_path = './data/president_polls.csv'
today = pd.Timestamp('today')

candidates = ['Donald Trump', 'Joe Biden']

# Load and process poll data
poll_data = load_poll_data(file_path)
pivot_avg_data = process_poll_data(poll_data, candidates, today)

# Calculate differential and determine the winner
pivot_avg_data = calculate_differential_and_winner(pivot_avg_data)

# Apply polling assumptions
pivot_avg_data = apply_polling_assumptions(pivot_avg_data)

# Add electoral votes to the data
pivot_avg_data = add_electoral_votes(pivot_avg_data, electoral_votes)

# Summarize electoral votes for each candidate
electoral_summary = summarize_electoral_votes(pivot_avg_data)

# Map full state names to abbreviations and prepare data for visualization
pivot_avg_data['state_code'] = pivot_avg_data.index.map(state_abbreviations)
pivot_avg_data['capped_diff'] = pivot_avg_data['differential'].clip(-30, 30)
pivot_avg_data['normalized_capped_diff'] = (pivot_avg_data['capped_diff'] + 30) / 60

# Plot the electoral college results
plot_electoral_college(pivot_avg_data, electoral_summary)

# Plot the choropleth map with capped differential colors and enhanced hover information
plot_choropleth(pivot_avg_data, electoral_summary)

# Simulate the election
simulation_results = simulate_election(pivot_avg_data, electoral_votes)

print("Simulation Results:")
print(simulation_results)
