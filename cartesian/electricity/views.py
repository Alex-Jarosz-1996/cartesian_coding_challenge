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

            return Response({"response": "Electricity data saved."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Server error: {e}."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteElectricityData(APIView):
    """
    API endpoint to retrieve electricity data if it exists.
    """

    def delete(self, request):
        try:
            num_rows_deleted = ElectricityDBService.delete_electricity_data_from_db()
            if num_rows_deleted:
                return Response({"error": f"Deleted {num_rows_deleted}."}, status=status.HTTP_200_OK)

            return Response({"response": "No electricity data to delete."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Server error: {e}."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MeanElectricityData(APIView):
    """
    API endpoint to perform mathematical calculations regarding the electricity data.
    """

    def get(self, request, state: str):
        try:
            data = ElectricityDBService.get_electricity_data_from_db(state=state)
            if data is None:
                return Response(
                    {"error": f"No electricity data found for state '{state.upper()}'."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            mean_price = round(sum(data) / len(data), 2)

            return Response(
                {"response": f"State: {state.upper()} | Mean price: ${mean_price}."}, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response({"error": f"Server error: {e}."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
