from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .api import get_electricity_data
from .db_methods import ElectricityDBService


class GetElectricityData(APIView):
    """
    API endpoint to retrieve electricity data.
    """

    def get(self, request):
        try:
            electricity_data = get_electricity_data()

            if electricity_data is None:
                return Response({"error": "No electricity data discovered."}, status=status.HTTP_404_NOT_FOUND)

            ElectricityDBService.add_electricity_data_to_db(data=electricity_data)

            return Response({"error": "Electricity data saved."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Server error: {e}."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
