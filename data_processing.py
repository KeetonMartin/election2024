# data_processing.py
import pandas as pd
from typing import List, Dict

def load_poll_data(file_path: str) -> pd.DataFrame:
    poll_data = pd.read_csv(file_path)
    poll_data['end_date'] = pd.to_datetime(poll_data['end_date'], format='%m/%d/%y', errors='coerce')
    return poll_data

def calculate_weight(end_date: pd.Timestamp, numeric_grade: float, today: pd.Timestamp) -> float:
    days_passed = (today - end_date).days
    age_weight = 0.5 ** (days_passed / 180)
    grade_weight = numeric_grade / 3.0
    return age_weight * grade_weight

def process_poll_data(poll_data: pd.DataFrame, candidates: List[str], today: pd.Timestamp) -> pd.DataFrame:
    poll_data['weight'] = poll_data.apply(lambda row: calculate_weight(row['end_date'], row['numeric_grade'], today), axis=1)
    
    relevant_columns = ['state', 'end_date', 'candidate_name', 'pct', 'weight', 'question_id']
    filtered_data = poll_data[relevant_columns]
    filtered_data = filtered_data[filtered_data['candidate_name'].isin(candidates)]
    
    # Calculate differentials per question_id
    differentials = filtered_data.pivot_table(index=['state', 'question_id'], columns='candidate_name', values='pct').dropna()
    differentials['question_id_differential'] = differentials['Donald Trump'] - differentials['Joe Biden']
    
    # Merge weights back into differentials
    weights = filtered_data[['state', 'question_id', 'weight']].drop_duplicates()
    differentials = differentials.reset_index().merge(weights, on=['state', 'question_id'])
    
    # Calculate weighted average differential per state
    differentials['weighted_diff'] = differentials['question_id_differential'] * differentials['weight']
    grouped_data = differentials.groupby('state').agg(
        total_weighted_diff=('weighted_diff', 'sum'),
        total_weight=('weight', 'sum')
    )
    grouped_data['weighted_avg_diff'] = grouped_data['total_weighted_diff'] / grouped_data['total_weight']
    
    # Create a pivot table similar to the original structure
    pivot_avg_data = grouped_data[['weighted_avg_diff']].rename(columns={'weighted_avg_diff': 'differential'})
    pivot_avg_data['Donald Trump'] = pivot_avg_data['differential'].apply(lambda x: max(0, x))
    pivot_avg_data['Joe Biden'] = pivot_avg_data['differential'].apply(lambda x: max(0, -x))
    pivot_avg_data['winner'] = pivot_avg_data['differential'].apply(lambda x: 'Donald Trump' if x > 0 else 'Joe Biden')
    
    return pivot_avg_data

def calculate_differential_and_winner(pivot_avg_data: pd.DataFrame) -> pd.DataFrame:
    pivot_avg_data['differential'] = pivot_avg_data.get('Donald Trump', 0) - pivot_avg_data.get('Joe Biden', 0)
    pivot_avg_data['winner'] = pivot_avg_data['differential'].apply(lambda x: 'Donald Trump' if x > 0 else 'Joe Biden')
    return pivot_avg_data

def add_electoral_votes(pivot_avg_data: pd.DataFrame, electoral_votes: Dict[str, int]) -> pd.DataFrame:
    pivot_avg_data['electoral_votes'] = pivot_avg_data.index.map(electoral_votes)
    return pivot_avg_data

def summarize_electoral_votes(pivot_avg_data: pd.DataFrame) -> pd.Series:
    return pivot_avg_data.groupby('winner')['electoral_votes'].sum()
