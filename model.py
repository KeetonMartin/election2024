import pandas as pd
from data_processing import load_poll_data, process_poll_data, calculate_differential_and_winner, add_electoral_votes, summarize_electoral_votes
from assumptions import apply_polling_assumptions
from electoral_votes import electoral_votes
from simulate_election import simulate_election
from state_abbreviations import state_abbreviations
from utils import plot_electoral_college, plot_choropleth

file_path = './data/president_polls.csv'
today = pd.Timestamp('today')

candidates = ['Donald Trump', 'Kamala Harris']

# Load and process poll data
poll_data = load_poll_data(file_path)
pivot_avg_data = process_poll_data(poll_data, candidates, today)

# Calculate differential and determine the winner
pivot_avg_data = calculate_differential_and_winner(pivot_avg_data)

# Apply polling assumptions
pivot_avg_data = apply_polling_assumptions(pivot_avg_data)

# Add electoral votes to the data
pivot_avg_data = add_electoral_votes(pivot_avg_data, electoral_votes)

# Debug: Print missing states
print("States in electoral votes but missing in pivot_avg_data:")
missing_states = set(electoral_votes.keys()) - set(pivot_avg_data.index)
print(missing_states)

# Simulate the election
win_probabilities, simulation_summary = simulate_election(pivot_avg_data, electoral_votes)

# Summarize electoral votes for each candidate
electoral_summary = summarize_electoral_votes(pivot_avg_data)

# Ensure the total number of electoral votes is correct
total_electoral_votes = electoral_summary.sum()
if total_electoral_votes != 538:
    raise ValueError(f"Total electoral votes are incorrect: {total_electoral_votes}. Should be 538.")

# Map full state names to abbreviations and prepare data for visualization
pivot_avg_data['state_code'] = pivot_avg_data.index.map(state_abbreviations)
pivot_avg_data['capped_diff'] = pivot_avg_data['differential'].clip(-30, 30)
pivot_avg_data['normalized_capped_diff'] = (pivot_avg_data['capped_diff'] + 30) / 60

# Plot the electoral college results with simulation summary and win probabilities
plot_electoral_college(pivot_avg_data, simulation_summary, win_probabilities)

# Plot the choropleth map with capped differential colors, enhanced hover information, and simulation summary
plot_choropleth(pivot_avg_data, simulation_summary, win_probabilities)

# Inspect a specific state for observability:
# Extract and display Vermont's polling average and the polls used
# vermont_polling_avg = pivot_avg_data.loc['Vermont']
# vermont_polls_used = poll_data[poll_data['state'] == 'Vermont']

# print("Vermont Polling Average:")
# print(vermont_polling_avg)

# print("\nPolls Used for Vermont's Calculation:")
# print(vermont_polls_used)
