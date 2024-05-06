# Prepare the hover text with enhanced details
def format_hover_text(state, trump, biden, differential, electoral_votes):
    if differential > 0:
        return f"{state}<br>Trump +{abs(differential):.1f}"
    elif differential < 0:
        return f"{state}<br>Biden +{abs(differential):.1f}"
    else:
        return f"{state}<br>Polling indicates no lead"
