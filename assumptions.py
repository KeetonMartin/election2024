# assumptions.py
import pandas as pd

def apply_polling_assumptions(polls_df: pd.DataFrame) -> pd.DataFrame:
    assumptions = {
        'District of Columbia': {'Donald Trump': 6.7, 'Kamala Harris': 90.0},
        'Hawaii': {'Donald Trump': 30.7, 'Kamala Harris': 63.4},
        'Delaware': {'Donald Trump': 39.77, 'Kamala Harris': 58.74},
        'Maryland': {'Donald Trump': 30.0, 'Kamala Harris': 56.0},
        'Wyoming': {'Donald Trump': 68.0, 'Kamala Harris': 15.0},
        'Idaho': {'Donald Trump': 55.0, 'Kamala Harris': 26.0},
        'New Jersey': {'Donald Trump': 39.0, 'Kamala Harris': 46.0},
        'South Carolina': {'Donald Trump': 51.0, 'Kamala Harris': 37.0},
        'Iowa': {'Donald Trump': 42.0, 'Kamala Harris': 36.0},
        'Rhode Island': {'Donald Trump': 37.0, 'Kamala Harris': 51.0},
        'Montana': {'Donald Trump': 51.0, 'Kamala Harris': 35.0},
        'Mississippi': {'Donald Trump': 54.0, 'Kamala Harris': 36.0},
        'Indiana': {'Donald Trump': 48.0, 'Kamala Harris': 29.0},
        'Kentucky': {'Donald Trump': 55.0, 'Kamala Harris': 26.0},
        'Vermont': {'Donald Trump': 28.0, 'Kamala Harris': 59.0},
        'Connecticut': {'Donald Trump': 40.0, 'Kamala Harris': 49.0},
        'Maine CD-2': {'Donald Trump': 42.0, 'Kamala Harris': 28.0},
        'Maine CD-1': {'Donald Trump': 31.0, 'Kamala Harris': 39.0},
        'Utah': {'Donald Trump': 54.0, 'Kamala Harris': 26.0},
        'South Dakota': {'Donald Trump': 55.0, 'Kamala Harris': 26.0},
        'Oregon': {'Donald Trump': 40.0, 'Kamala Harris': 45.0},
        'Tennessee': {'Donald Trump': 58.0, 'Kamala Harris': 24.0},
        'Alabama': {'Donald Trump': 57.0, 'Kamala Harris': 38.0},
        'Kansas': {'Donald Trump': 50.0, 'Kamala Harris': 37.0},
        'Nebraska': {'Donald Trump': 42.0, 'Kamala Harris': 34.0},
        'Massachusetts': {'Donald Trump': 27.0, 'Kamala Harris': 48.0},
        'West Virginia': {'Donald Trump': 55.0, 'Kamala Harris': 28.0},
        'Louisiana': {'Donald Trump': 48.0, 'Kamala Harris': 33.0},
        'Arkansas': {'Donald Trump': 57.0, 'Kamala Harris': 24.0},
        'Missouri': {'Donald Trump': 50.0, 'Kamala Harris': 35.0},
        'New Mexico': {'Donald Trump': 41.0, 'Kamala Harris': 48.0},
        'Oklahoma': {'Donald Trump': 56.0, 'Kamala Harris': 24.0},
        'Colorado': {'Donald Trump': 44.0, 'Kamala Harris': 48.0},
        'North Dakota': {'Donald Trump': 62.0, 'Kamala Harris': 28.0},
        'Alaska': {'Donald Trump': 49.0, 'Kamala Harris': 26.0},
        'Illinois': {'Donald Trump': 34.0, 'Kamala Harris': 43.0},
        'Nebraska CD-2': {'Donald Trump': 45.6, 'Kamala Harris': 52.4},
        'Nebraska CD-1': {'Donald Trump': 56.4, 'Kamala Harris': 41.3},
        'Nebraska CD-3': {'Donald Trump': 75.6, 'Kamala Harris': 22.4}
    }

    for region, values in assumptions.items():
        if region in polls_df.index:
            polls_df.at[region, 'Donald Trump'] = values['Donald Trump']
            polls_df.at[region, 'Kamala Harris'] = values['Kamala Harris']
            polls_df.at[region, 'differential'] = values['Donald Trump'] - values['Kamala Harris']
            polls_df.at[region, 'winner'] = 'Donald Trump' if values['Donald Trump'] > values['Kamala Harris'] else 'Kamala Harris'
        else:
            new_row = pd.DataFrame({
                'Donald Trump': [values['Donald Trump']],
                'Kamala Harris': [values['Kamala Harris']],
                'differential': [values['Donald Trump'] - values['Kamala Harris']],
                'winner': ['Donald Trump' if values['Donald Trump'] > values['Kamala Harris'] else 'Kamala Harris']
            }, index=[region])
            polls_df = pd.concat([polls_df, new_row])

    return polls_df
