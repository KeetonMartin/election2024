# assumptions.py
import pandas as pd

def apply_polling_assumptions(polls_df: pd.DataFrame) -> pd.DataFrame:
    assumptions = {
        'District of Columbia': {'Donald Trump': 6.7, 'Joe Biden': 90.0},
        'Hawaii': {'Donald Trump': 30.7, 'Joe Biden': 63.4},
        'Delaware': {'Donald Trump': 39.77, 'Joe Biden': 58.74},
        'Nebraska CD-2': {'Donald Trump': 45.6, 'Joe Biden': 52.4},
        'Nebraska CD-1': {'Donald Trump': 56.4, 'Joe Biden': 41.3},
        'Nebraska CD-3': {'Donald Trump': 75.6, 'Joe Biden': 22.4}
    }

    for region, values in assumptions.items():
        if region in polls_df.index:
            polls_df.at[region, 'Donald Trump'] = values['Donald Trump']
            polls_df.at[region, 'Joe Biden'] = values['Joe Biden']
            polls_df.at[region, 'differential'] = values['Donald Trump'] - values['Joe Biden']
            polls_df.at[region, 'winner'] = 'Donald Trump' if values['Donald Trump'] > values['Joe Biden'] else 'Joe Biden'
        else:
            new_row = pd.DataFrame({
                'Donald Trump': [values['Donald Trump']],
                'Joe Biden': [values['Joe Biden']],
                'differential': [values['Donald Trump'] - values['Joe Biden']],
                'winner': ['Donald Trump' if values['Donald Trump'] > values['Joe Biden'] else 'Joe Biden']
            }, index=[region])
            polls_df = pd.concat([polls_df, new_row])

    return polls_df
