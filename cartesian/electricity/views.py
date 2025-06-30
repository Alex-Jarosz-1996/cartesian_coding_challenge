from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class GetElectricityData(APIView):
    """
    API endpoint to retrieve electricity data.
    """

    def get(self, request):
        try:
            return Response({"error": "Electricity data saved."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Server error: {e}."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
