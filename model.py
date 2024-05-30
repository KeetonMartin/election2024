# main.py
import pandas as pd
from data_processing import load_poll_data, process_poll_data, calculate_differential_and_winner, add_electoral_votes, summarize_electoral_votes
from assumptions import apply_polling_assumptions
from utils import plot_electoral_college, plot_choropleth

file_path = './data/president_polls.csv'
today = pd.Timestamp('today')

electoral_votes = {
    'Alabama': 9, 'Alaska': 3, 'Arizona': 11, 'Arkansas': 6,
    'California': 54, 'Colorado': 10, 'Connecticut': 7, 'Delaware': 3,
    'District of Columbia': 3, 'Florida': 30, 'Georgia': 16, 'Hawaii': 4,
    'Idaho': 4, 'Illinois': 19, 'Indiana': 11, 'Iowa': 6,
    'Kansas': 6, 'Kentucky': 8, 'Louisiana': 8, 'Maine CD-1': 1, 'Maine CD-2': 1,
    'Maryland': 10, 'Massachusetts': 11, 'Michigan': 15, 'Minnesota': 10,
    'Mississippi': 6, 'Missouri': 10, 'Montana': 4, 'Nebraska CD-1': 1, 'Nebraska CD-2': 1, 'Nebraska CD-3': 1,
    'Nevada': 6, 'New Hampshire': 4, 'New Jersey': 14, 'New Mexico': 5,
    'New York': 28, 'North Carolina': 16, 'North Dakota': 3, 'Ohio': 17,
    'Oklahoma': 7, 'Oregon': 8, 'Pennsylvania': 19, 'Rhode Island': 4,
    'South Carolina': 9, 'South Dakota': 3, 'Tennessee': 11, 'Texas': 40,
    'Utah': 6, 'Vermont': 3, 'Virginia': 13, 'Washington': 12,
    'West Virginia': 4, 'Wisconsin': 10, 'Wyoming': 3, 'Maine': 2, 'Nebraska': 2
}

state_abbreviations = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'District of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI',
    'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME',
    'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
    'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE',
    'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
    'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI',
    'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
    'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

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
