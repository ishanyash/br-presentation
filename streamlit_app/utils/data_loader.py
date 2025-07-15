import os

import warnings
from functools import lru_cache

import pandas as pd
import pgeocode

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'investment_analysis_phase3.csv')

nomi = pgeocode.Nominatim('GB')


@lru_cache(maxsize=None)
def _geocode_postcode(postcode):
    """Query latitude and longitude for a postcode with caching."""
    result = nomi.query_postal_code(str(postcode))
    return result.latitude, result.longitude


@lru_cache(maxsize=1)
def load_data(drop_invalid: bool = False) -> pd.DataFrame:
    """Load dataset and attach latitude/longitude using pgeocode.

    Parameters
    ----------
    drop_invalid: bool, optional
        If ``True``, rows for which geocoding fails are dropped. Otherwise the
        coordinates are filled with ``0, 0`` and a warning is emitted.
    """

    df = pd.read_csv(DATA_PATH)

    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        latitudes = []
        longitudes = []
        invalid_idx = []

        for idx, postcode in df['postcode'].items():
            lat, lon = _geocode_postcode(postcode)
            if pd.isna(lat) or pd.isna(lon):
                if drop_invalid:
                    invalid_idx.append(idx)
                    continue
                warnings.warn(
                    f"Coordinates not found for postcode {postcode}; using 0,0"
                )
                lat, lon = 0.0, 0.0
            latitudes.append(lat)
            longitudes.append(lon)

        df.loc[df.index.difference(invalid_idx), 'latitude'] = latitudes
        df.loc[df.index.difference(invalid_idx), 'longitude'] = longitudes

        if drop_invalid and invalid_idx:
            warnings.warn(
                f"Dropping {len(invalid_idx)} rows with missing geocode results"
            )
            df = df.drop(index=invalid_idx).reset_index(drop=True)
    return df
