from typing import Optional

import pandas as pd
from decouple import config


def get_electricity_data() -> Optional[pd.DataFrame]:
    """
    Retrieves csv electricity data.
    """
    try:
        GITHUB_CSV_URL = config("GITHUB_CSV_URL")
        return pd.read_csv(GITHUB_CSV_URL, index_col=0)

    except Exception:
        return None
