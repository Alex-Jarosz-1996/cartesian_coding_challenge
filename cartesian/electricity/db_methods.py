import pandas as pd
from django.db import transaction

from .models import ElectricityModel


class ElectricityDBService:

    REQUIRED_COLUMNS = ["state", "price", "timestamp"]

    @staticmethod
    def add_electricity_data_to_db(data: pd.DataFrame):
        """
        Adds electricity to the db.
        """
        try:
            # ensuring data is not empty
            if data is None or data.empty:
                raise ValueError("No electricity data received.")

            # ensuring all required fields present
            for required_field in ElectricityDBService.REQUIRED_COLUMNS:
                if required_field not in data.columns:
                    raise ValueError(
                        f"Column '{required_field}' not in required fields: '{ElectricityDBService.REQUIRED_COLUMNS}'"
                    )

            # creating object for bulk importing
            objects = [
                ElectricityModel(
                    state=row["state"],
                    price=float(str(row["price"])),
                    timestamp=row["timestamp"],
                )
                for _, row in data.iterrows()
            ]

            with transaction.atomic():
                ElectricityModel.objects.bulk_create(
                    objects,
                    batch_size=1_000,
                )

        except Exception as e:
            raise e
