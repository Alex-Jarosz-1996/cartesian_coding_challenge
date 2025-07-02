from typing import Optional

import pandas as pd
from django.db import transaction

from .models import ElectricityModel


class ElectricityDBService:

    REQUIRED_COLUMNS = ["price", "timestamp"]

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
                    state=idx,
                    price=float(str(row["price"])),
                    timestamp=row["timestamp"],
                )
                for idx, row in data.iterrows()
            ]

            with transaction.atomic():
                ElectricityModel.objects.bulk_create(
                    objects,
                    batch_size=1_000,
                )

        except Exception as e:
            raise e

    @staticmethod
    def delete_electricity_data_from_db() -> int:
        """
        Deletes all electricity data from the db.
        """
        try:
            with transaction.atomic():
                rows_deleted, _ = ElectricityModel.objects.all().delete()

                return rows_deleted

        except Exception as e:
            raise e

    @staticmethod
    def get_electricity_data_from_db(state: str) -> Optional[list]:
        """
        Retrieves electricity data from db.
        """
        try:
            prices = ElectricityModel.objects.filter(
                state__iexact=state
            ).values_list(  # using state__iexact for case insensitive matching
                "price", flat=True
            )  # flat=True for tuple -> list conversion
            return list(prices) if prices.exists() else None

        except Exception as e:
            raise e
