import datetime
from unittest.mock import patch

import pandas as pd
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .db_methods import ElectricityDBService
from .models import ElectricityModel


class ElectricityDBServiceTests(APITestCase):
    """Unit tests for the DB service layer."""

    def test_add_electricity_data_empty_dataframe_raises(self):
        """Expect ValueError on empty DataFrame."""
        with self.assertRaises(ValueError):
            ElectricityDBService.add_electricity_data_to_db(pd.DataFrame())


class GetElectricityDataAPITests(APITestCase):
    """Tests for the /api/electricity/get_data/ endpoint."""

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("get_data")  # resolves to /api/electricity/get_data/

    @patch("electricity.views.get_electricity_data")
    def test_get_electricity_data_success(self, mock_get_data):
        """API returns 201 response."""
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
        """API returns 404 response."""
        mock_get_data.return_value = None

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ElectricityModel.objects.count(), 0)


class DeleteElectricityDataAPITests(APITestCase):
    """Tests for the /api/electricity/delete_data/ endpoint."""

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("delete_data")  # resolves to /api/electricity/delete_data/

    def test_delete_electricity_data_success(self):
        """API returns 200 response."""
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
        """API returns 200 response."""
        self.assertEqual(ElectricityModel.objects.count(), 0)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("No electricity data to delete", response.json()["response"])


class MeanElectricityDataAPITests(APITestCase):
    """Tests for the /api/electricity/get_mean/<state>/ endpoint."""

    @classmethod
    def setUpTestData(cls):
        cls.url = "get_mean"  # resolves to /api/electricity/get_mean/

    def test_mean_price_success(self):
        """API returns 201 response."""
        state = "tas"
        prices = [float("90.00"), float("60.00"), float("75.00")]
        timestamps = [
            timezone.make_aware(datetime.datetime(2025, 6, 24, 0, 0)),
            timezone.make_aware(datetime.datetime(2025, 6, 24, 0, 30)),
            timezone.make_aware(datetime.datetime(2025, 6, 24, 1, 0)),
        ]

        ElectricityModel.objects.bulk_create(
            ElectricityModel(state=state.upper(), price=p, timestamp=t) for p, t in zip(prices, timestamps)
        )

        expected_mean = round(sum(prices) / len(prices), 2)  # 75.00
        url = reverse(self.url, args=[state])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(f"Mean price: ${expected_mean}", response.json()["response"])

    def test_mean_price_no_data(self):
        """API returns 404 response."""
        url = reverse(self.url, args=["qld"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("No electricity data found", response.json()["error"])
