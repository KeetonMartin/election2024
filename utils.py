def format_hover_text(state, trump, biden, differential, electoral_votes, trump_pollster, biden_pollster, trump_date, biden_date):
    if differential > 0:
        return f"{state}<br>Trump +{abs(differential):.1f}<br>Pollster: {trump_pollster}<br>Date: {trump_date.date()}"
    elif differential < 0:
        return f"{state}<br>Biden +{abs(differential):.1f}<br>Pollster: {biden_pollster}<br>Date: {biden_date.date()}"
    else:
        return f"{state}<br>Polling indicates no lead"
