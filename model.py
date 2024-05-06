import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load the dataset
file_path = './data/president_polls3.csv'
poll_data = pd.read_csv(file_path)

# Convert 'end_date' to datetime with the correct format
poll_data['end_date'] = pd.to_datetime(poll_data['end_date'], format='%m/%d/%y', errors='coerce')

# Determine today's date for reference
today = pd.Timestamp('today')

# Define a function to calculate weights based on the age of the poll
# Using exponential decay, where weight decreases by half every 180 days (half-life)
def calculate_weight(end_date):
    days_passed = (today - end_date).days
    return 0.5 ** (days_passed / 180)

# Apply the weight function to each poll
poll_data['weight'] = poll_data['end_date'].apply(calculate_weight)

# Filter and focus on relevant columns and candidates
relevant_columns = ['state', 'end_date', 'candidate_name', 'pct', 'weight']
candidates = ['Donald Trump', 'Joe Biden']
filtered_data = poll_data[relevant_columns]
filtered_data = filtered_data[filtered_data['candidate_name'].isin(candidates)]

# Calculate weighted percentages
filtered_data['weighted_pct'] = filtered_data['pct'] * filtered_data['weight']

# Pivot data to compare Trump and Biden in each row, summing weighted percentages
pivot_data = filtered_data.pivot_table(index=['state', 'end_date'], columns='candidate_name', values='weighted_pct', aggfunc='sum')

# Pivot data to compare Trump and Biden in each row
pivot_data = filtered_data.pivot_table(index=['state', 'end_date'], columns='candidate_name', values='pct', aggfunc='max')
pivot_data = pivot_data.fillna(0)  # Fill missing values with 0
# Calculate differential and determine the winner with weighted percentages
pivot_data['differential'] = pivot_data.get('Donald Trump', 0) - pivot_data.get('Joe Biden', 0)
pivot_data['winner'] = pivot_data['differential'].apply(lambda x: 'Donald Trump' if x > 0 else 'Joe Biden')

# Get the latest poll for each state
latest_polls = pivot_data.groupby('state').last().reset_index()

# Check if Hawaii is in the latest polls, if not, assume it goes for Joe Biden
# if 'Hawaii' not in latest_polls['state'].values:
#     hawaii_data = {'state': 'Hawaii', 'end_date': pd.to_datetime('2024-11-04'), 'Donald Trump': 0, 'Joe Biden': 100,
#                    'differential': -100, 'winner': 'Joe Biden'}
#     hawaii_df = pd.DataFrame([hawaii_data])
#     latest_polls = pd.concat([latest_polls, hawaii_df], ignore_index=True)

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
plt.figure(figsize=(12, 6))
plt.bar(states, latest_polls['electoral_votes'], color=color_map)
plt.xticks(rotation=90)  # Rotate state labels for better visibility
plt.title('2024 Electoral College Prediction')
plt.xlabel('States')
plt.ylabel('Electoral Votes')
plt.show()

print(electoral_summary)

# State abbreviation mapping
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

# Check Hawaii's data
print(latest_polls[latest_polls['state'] == 'Hawaii'])

# Map full state names to abbreviations
latest_polls['state_code'] = latest_polls['state'].map(state_abbreviations)

# Update Plotly visualization with state codes
fig = px.choropleth(latest_polls,
                    locations='state_code',  # Use state abbreviations
                    locationmode="USA-states",
                    color='winner',
                    hover_name='state',
                    color_discrete_map={'Donald Trump': 'red', 'Joe Biden': 'blue'},
                    scope="usa",
                    title='2024 Electoral College Prediction')
fig.show()
