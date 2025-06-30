import datetime
from unittest.mock import patch

import pandas as pd
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .db_methods import ElectricityDBService
from .models import ElectricityModel


class GetElectricityDataAPITests(APITestCase):
    """Tests for the /api/electricity/get/ endpoint."""

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("get_data")  # resolves to /api/electricity/get/

    @patch("electricity.views.get_electricity_data")
    def test_get_electricity_data_success(self, mock_get_data):
        """API returns 201 and rows are inserted when data is present."""
        sample_df = pd.DataFrame(
            {
                "price": [81.52, 76.32],
                "timestamp": [
                    timezone.make_aware(datetime.datetime(2025, 6, 24, 0, 0)),
                    timezone.make_aware(datetime.datetime(2025, 6, 24, 0, 30)),
                ],
            },
            index=pd.Index(["Vic", "Vic"], name="state"),
        )

        mock_get_data.return_value = sample_df

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ElectricityModel.objects.count(), 2)

        obj = ElectricityModel.objects.first()
        self.assertEqual(obj.state, "Vic")
        self.assertEqual(obj.price, float("81.52"))

    @patch("electricity.views.get_electricity_data")
    def test_get_electricity_data_empty(self, mock_get_data):
        """API returns 404 when the data source returns None."""
        mock_get_data.return_value = None

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ElectricityModel.objects.count(), 0)


class DeleteElectricityDataAPITests(APITestCase):
    """Tests for the /api/electricity/delete/ endpoint."""

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("delete_data")

    def test_delete_electricity_data_success(self):
        ElectricityModel.objects.bulk_create(
            [
                ElectricityModel(
                    state="VIC",
                    price=81.52,
                    timestamp=timezone.make_aware(datetime.datetime(2025, 6, 24, 0, 0)),
                ),
                ElectricityModel(
                    state="VIC",
                    price=76.32,
                    timestamp=timezone.make_aware(datetime.datetime(2025, 6, 24, 0, 30)),
                ),
            ]
        )

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Deleted 2", response.json()["error"])
        self.assertEqual(ElectricityModel.objects.count(), 0)

    def test_delete_electricity_data_no_rows(self):
        self.assertEqual(ElectricityModel.objects.count(), 0)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("No electricity data to delete", response.json()["error"])


class ElectricityDBServiceTests(APITestCase):
    """Unit tests for the DB service layer."""

    def test_add_electricity_data_empty_dataframe_raises(self):
        """Expect ValueError on empty DataFrame."""
        with self.assertRaises(ValueError):
            ElectricityDBService.add_electricity_data_to_db(pd.DataFrame())
