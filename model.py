import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.offline as pyo

from assumptions import apply_polling_assumptions
from utils import format_hover_text
import datetime

# Load the dataset
file_path = './data/president_polls3.csv'
poll_data = pd.read_csv(file_path)

# Convert 'end_date' to datetime with the correct format
poll_data['end_date'] = pd.to_datetime(poll_data['end_date'], format='%m/%d/%y', errors='coerce')

# Determine today's date for reference
today = pd.Timestamp('today')

# Define a function to calculate weights based on the age of the poll
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

# Group by state and candidate, then calculate the sum of weighted percentages and sum of weights
grouped_data = filtered_data.groupby(['state', 'candidate_name']).agg(
    total_weighted_pct=('weighted_pct', 'sum'),
    total_weight=('weight', 'sum')
).reset_index()

# Calculate the weighted average
grouped_data['weighted_avg_pct'] = grouped_data['total_weighted_pct'] / grouped_data['total_weight']

# Pivot data to compare Trump and Biden in each row
pivot_avg_data = grouped_data.pivot_table(index='state', columns='candidate_name', values='weighted_avg_pct', aggfunc='max')
pivot_avg_data.fillna(0, inplace=True)

# Calculate differential and determine the winner with weighted averages
pivot_avg_data['differential'] = pivot_avg_data.get('Donald Trump', 0) - pivot_avg_data.get('Joe Biden', 0)
pivot_avg_data['winner'] = pivot_avg_data['differential'].apply(lambda x: 'Donald Trump' if x > 0 else 'Joe Biden')

# Apply polling assumptions
pivot_avg_data = apply_polling_assumptions(pivot_avg_data)

# Electoral votes mapping, adjusted for district-based voting in Nebraska and Maine
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

# Map electoral votes to the averaged data
pivot_avg_data['electoral_votes'] = pivot_avg_data.index.map(electoral_votes)

# Summarize electoral votes for each candidate
electoral_summary = pivot_avg_data.groupby('winner')['electoral_votes'].sum()

# Visualization
color_map = pivot_avg_data['winner'].map({'Donald Trump': 'red', 'Joe Biden': 'blue'}).tolist()
states = pivot_avg_data.index.tolist()
plt.figure(figsize=(12, 6))
plt.bar(states, pivot_avg_data['electoral_votes'], color=color_map)
plt.xticks(rotation=90)
plt.title('2024 Electoral College Prediction')
plt.xlabel('States')
plt.ylabel('Electoral Votes')
plt.show()

print(electoral_summary)

# Other parts of your visualization and code logic remain the same.

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

# Cap the 'differential' at -30 and 30 in the pivot_avg_data
pivot_avg_data['capped_diff'] = pivot_avg_data['differential'].clip(-30, 30)

# Normalize the capped differential from 0 to 1 for color mapping
# The minimum is -30 and maximum is 30
pivot_avg_data['normalized_capped_diff'] = (pivot_avg_data['capped_diff'] + 30) / 60  # This shifts and scales the values

# Map full state names to abbreviations
pivot_avg_data['state_code'] = pivot_avg_data.index.map(state_abbreviations)

# Prepare the hover text with enhanced details, ensuring that 'hover_text' is a defined function in your utils
# Assuming your DataFrame is pivot_avg_data and 'state' is the index
pivot_avg_data['hover_text'] = pivot_avg_data.apply(lambda x: format_hover_text(x.name, x['Donald Trump'], x['Joe Biden'], x['differential'], x['electoral_votes']), axis=1)

# Create a custom color scale that reflects the differential magnitude
color_scale = [
    [0.0, "blue"],   # Favors Biden strongly
    [0.5, "white"],  # Neutral
    [1.0, "red"]     # Favors Trump strongly
]

# Update Plotly visualization with capped differential colors and enhanced hover information
fig = px.choropleth(
    pivot_avg_data,
    locations='state_code',  # Use state abbreviations
    locationmode="USA-states",
    color='normalized_capped_diff',  # Use normalized capped differential for coloring
    hover_name='hover_text',  # Use custom hover text
    color_continuous_scale=color_scale,  # Use the updated color scale
    scope="usa",
    title='2024 Electoral College Prediction'
)

# Add an annotation for electoral summary

electoral_summary_text = "<br>".join([f"{winner}: {votes} votes" for winner, votes in electoral_summary.items()])
today = datetime.date.today().strftime("%B %d, %Y")
updated_text = f"Last Updated: {today}"
fig.add_annotation(
    xref="paper", yref="paper",
    x=0.5, y=0.1,  # Adjust positioning based on your layout preferences
    text=f"Electoral Vote Summary:<br>{electoral_summary_text}<br>{updated_text}",
    showarrow=False,
    align="center",
    bgcolor="rgba(255, 255, 255, 0.8)",  # Semi-transparent white background
    font=dict(size=16, color="black")
)

# Set dark theme and adjust color bar title
fig.update_layout(template='plotly_dark')
# fig.update_layout(coloraxis_colorbar=None)
pyo.plot(fig, filename='index.html', auto_open=False)

fig.show()