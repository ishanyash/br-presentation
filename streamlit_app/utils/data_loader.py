import os
from functools import lru_cache

import pandas as pd
import pgeocode

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'investment_analysis_phase3.csv')

@lru_cache(maxsize=1)
def load_data():
    """Load dataset and attach latitude/longitude using pgeocode."""
    df = pd.read_csv(DATA_PATH)
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        nomi = pgeocode.Nominatim('GB')
        df['latitude'] = df['postcode'].apply(lambda x: nomi.query_postal_code(str(x)).latitude)
        df['longitude'] = df['postcode'].apply(lambda x: nomi.query_postal_code(str(x)).longitude)
    return df
