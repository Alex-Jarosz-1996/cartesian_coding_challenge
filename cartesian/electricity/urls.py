from django.urls import path

from .views import DeleteElectricityData, GetElectricityData

urlpatterns = [
    path("get", GetElectricityData.as_view(), name="get_data"),
    path("delete", DeleteElectricityData.as_view(), name="delete_data"),
]
