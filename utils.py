# utils.py
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.offline as pyo
import datetime
import pandas as pd

def format_hover_text(state: str, trump: float, biden: float, differential: float, electoral_votes: int) -> str:
    if differential > 0:
        return f"{state}<br>Trump +{abs(differential):.1f}"
    elif differential < 0:
        return f"{state}<br>Biden +{abs(differential):.1f}"
    else:
        return f"{state}<br>Polling indicates no lead"

def plot_electoral_college(pivot_avg_data: pd.DataFrame, electoral_summary: pd.Series):
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

def plot_choropleth(pivot_avg_data: pd.DataFrame, electoral_summary: pd.Series):
    color_scale = [
        [0.0, "blue"],
        [0.5, "white"],
        [1.0, "red"]
    ]
    pivot_avg_data['hover_text'] = pivot_avg_data.apply(lambda x: format_hover_text(x.name, x['Donald Trump'], x['Joe Biden'], x['differential'], x['electoral_votes']), axis=1)
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
    electoral_summary_text = "<br>".join([f"{winner}: {votes} votes" for winner, votes in electoral_summary.items()])
    today = datetime.date.today().strftime("%B %d, %Y")
    updated_text = f"Last Updated: {today}"
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.5, y=0.1,
        text=f"Electoral Vote Summary:<br>{electoral_summary_text}<br>{updated_text}",
        showarrow=False,
        align="center",
        bgcolor="rgba(255, 255, 255, 0.8)",
        font=dict(size=16, color="black")
    )
    fig.update_layout(
        template='plotly_dark',
        coloraxis_showscale=False
    )
    pyo.plot(fig, filename='index.html', auto_open=False)
    fig.show()