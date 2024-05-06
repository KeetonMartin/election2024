import pandas as pd

def apply_polling_assumptions(polls_df):
    # Define specific states or districts with known political leanings
    assumptions = {
        'District of Columbia': {'Donald Trump': 0, 'Joe Biden': 100},
        'Hawaii': {'Donald Trump': 0, 'Joe Biden': 100},
        'Nebraska CD-2': {'Donald Trump': 0, 'Joe Biden': 100},
        'Nebraska CD-1': {'Donald Trump': 100, 'Joe Biden': 0},
        'Nebraska CD-3': {'Donald Trump': 100, 'Joe Biden': 0}
    }

    # Update the dataframe with assumptions
    for region, values in assumptions.items():
        if region not in polls_df['state'].values:
            new_data = {
                'state': region,
                'end_date': pd.to_datetime('2024-11-04'),
                'Donald Trump': values['Donald Trump'],
                'Joe Biden': values['Joe Biden'],
                'differential': values['Donald Trump'] - values['Joe Biden'],
                'winner': 'Donald Trump' if values['Donald Trump'] > values['Joe Biden'] else 'Joe Biden'
            }
            polls_df = pd.concat([polls_df, pd.DataFrame([new_data])], ignore_index=True)
    return polls_df