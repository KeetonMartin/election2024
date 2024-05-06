# Prepare the hover text with enhanced details
def format_hover_text(row):
    if row['differential'] > 0:
        return f"{row['state']}<br>Trump leads by {abs(row['differential']):.2f}<br>Electoral Votes: {row['electoral_votes']}"
    elif row['differential'] < 0:
        return f"{row['state']}<br>Biden leads by {abs(row['differential']):.2f}<br>Electoral Votes: {row['electoral_votes']}"
    else:
        return f"{row['state']}<br>Polling indicates Tie<br>Electoral Votes: {row['electoral_votes']}"