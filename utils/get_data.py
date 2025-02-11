from app_store_scraper import AppStore
import pandas as pd
from utils.data_cleaning import data_cleaning

def get_data(app_name='nebula-horoscope-astrology', app_id='1459969523'):

    nebula = AppStore(country='us', app_name=app_name, app_id=app_id)
    nebula.review(how_many=100)
    selected_columns = ['date', 'review', 'rating', 'title']
    nebula_df = pd.DataFrame(nebula.reviews)
    selected_data = nebula_df[selected_columns]
    selected_data = data_cleaning(selected_data)
    df_sampled = selected_data.sample(n=100, replace=True, random_state=42)
    df_sampled['rating'] = pd.to_numeric(df_sampled['rating'], errors='coerce').astype('int')
    return df_sampled

def stats_data(data):
    stats = data['rating'].describe()
    return stats
