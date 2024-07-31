import matplotlib.pyplot as plt
import plotly.express as px
import plotly.offline as pyo
import datetime
import pandas as pd

def format_hover_text(state: str, trump: float, harris: float, differential: float, electoral_votes: int) -> str:
    if differential > 0:
        return f"{state}<br>Trump +{abs(differential):.1f}"
    elif differential < 0:
        return f"{state}<br>Harris +{abs(differential):.1f}"
    else:
        return f"{state}<br>Polling indicates no lead"

def plot_electoral_college(pivot_avg_data: pd.DataFrame, simulation_summary: pd.Series, win_probabilities: dict):
    color_map = pivot_avg_data['winner'].map({'Donald Trump': 'red', 'Kamala Harris': 'blue'}).tolist()
    states = pivot_avg_data.index.tolist()
    plt.figure(figsize=(12, 6))
    plt.bar(states, pivot_avg_data['electoral_votes'], color=color_map)
    plt.xticks(rotation=90)
    plt.title('2024 Electoral College Prediction')
    plt.xlabel('States')
    plt.ylabel('Electoral Votes')
    plt.show()
    print(simulation_summary)
    print(f"Donald Trump: {win_probabilities['Donald Trump']:.1%} chance of victory")
    print(f"Kamala Harris: {win_probabilities['Kamala Harris']:.1%} chance of victory")

def plot_choropleth(pivot_avg_data: pd.DataFrame, simulation_summary: pd.Series, win_probabilities: dict):
    color_scale = [
        [0.0, "blue"],
        [0.5, "white"],
        [1.0, "red"]
    ]
    pivot_avg_data['hover_text'] = pivot_avg_data.apply(lambda x: format_hover_text(x.name, x['Donald Trump'], x['Kamala Harris'], x['differential'], x['electoral_votes']), axis=1)
    fig = px.choropleth(
        pivot_avg_data,
        locations='state_code',
        locationmode="USA-states",
        color='normalized_capped_diff',
        hover_name='hover_text',
        color_continuous_scale=color_scale,
        scope="usa",
        title='2024 Electoral College Prediction'
    )
    simulation_summary_text = "<br>".join([f"{winner}: {votes:.1f} votes" for winner, votes in simulation_summary.items()])
    today = datetime.date.today().strftime("%B %d, %Y")
    updated_text = (
        f"Electoral Vote Summary from Simulation:<br>{simulation_summary_text}<br>"
        f"Donald Trump: {win_probabilities['Donald Trump']:.1%} chance of victory<br>"
        f"Kamala Harris: {win_probabilities['Kamala Harris']:.1%} chance of victory<br>"
        f"Last Updated: {today}"
    )
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.5, y=0.01,
        text=updated_text,
        showarrow=False,
        align="center",
        bgcolor="rgba(255, 255, 255, 0.6)",
        font=dict(size=16, color="black")
    )
    fig.update_layout(
        template='plotly_dark',
        coloraxis_showscale=False
    )
    pyo.plot(fig, filename='index.html', auto_open=False)
    fig.show()
