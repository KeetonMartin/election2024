import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = './data/president_polls.csv'
poll_data = pd.read_csv(file_path)

# Filter and focus on relevant columns and candidates
relevant_columns = ['state', 'end_date', 'candidate_name', 'pct']
candidates = ['Donald Trump', 'Joe Biden']
filtered_data = poll_data[relevant_columns]
filtered_data = filtered_data[filtered_data['candidate_name'].isin(candidates)]

# Convert 'end_date' to datetime
# Specify the format if you know it, e.g., '%Y-%m-%d'
filtered_data['end_date'] = pd.to_datetime(filtered_data['end_date'], format='%Y-%m-%d', errors='coerce')

# Pivot data to compare Trump and Biden in each row
pivot_data = filtered_data.pivot_table(index=['state', 'end_date'], columns='candidate_name', values='pct', aggfunc='max')
pivot_data = pivot_data.fillna(0)  # Fill missing values with 0
pivot_data['differential'] = pivot_data.get('Donald Trump', 0) - pivot_data.get('Joe Biden', 0)
pivot_data['winner'] = pivot_data['differential'].apply(lambda x: 'Donald Trump' if x > 0 else 'Joe Biden')

# Get the latest poll for each state
latest_polls = pivot_data.groupby('state').last().reset_index()

# Electoral votes mapping
electoral_votes = {
    'Alabama': 9, 'Alaska': 3, 'Arizona': 11, 'Arkansas': 6,
    'California': 54, 'Colorado': 10, 'Connecticut': 7, 'Delaware': 3,
    'District of Columbia': 3, 'Florida': 30, 'Georgia': 16, 'Hawaii': 4,
    'Idaho': 4, 'Illinois': 19, 'Indiana': 11, 'Iowa': 6,
    'Kansas': 6, 'Kentucky': 8, 'Louisiana': 8, 'Maine': 4,
    'Maryland': 10, 'Massachusetts': 11, 'Michigan': 15, 'Minnesota': 10,
    'Mississippi': 6, 'Missouri': 10, 'Montana': 4, 'Nebraska': 5,
    'Nevada': 6, 'New Hampshire': 4, 'New Jersey': 14, 'New Mexico': 5,
    'New York': 28, 'North Carolina': 16, 'North Dakota': 3, 'Ohio': 17,
    'Oklahoma': 7, 'Oregon': 8, 'Pennsylvania': 19, 'Rhode Island': 4,
    'South Carolina': 9, 'South Dakota': 3, 'Tennessee': 11, 'Texas': 40,
    'Utah': 6, 'Vermont': 3, 'Virginia': 13, 'Washington': 12,
    'West Virginia': 4, 'Wisconsin': 10, 'Wyoming': 3
}

# Map electoral votes to the latest data
latest_polls['electoral_votes'] = latest_polls['state'].map(electoral_votes)

# Summarize electoral votes for each candidate
electoral_summary = latest_polls.groupby('winner')['electoral_votes'].sum()

# Visualization
color_map = latest_polls['winner'].map({'Donald Trump': 'red', 'Joe Biden': 'blue'}).tolist()
states = latest_polls['state'].tolist()
plt.bar(states, latest_polls['electoral_votes'], color=color_map)
plt.xticks(rotation=90)  # Rotate state labels for better visibility
plt.title('2024 Electoral College Prediction')
plt.xlabel('States')
plt.ylabel('Electoral Votes')
plt.show()

print(electoral_summary)
