from django.urls import path

from .views import DeleteElectricityData, GetElectricityData, MeanElectricityData

urlpatterns = [
    path("get_data", GetElectricityData.as_view(), name="get_data"),
    path("delete_data", DeleteElectricityData.as_view(), name="delete_data"),
    path("get_mean/<str:state>", MeanElectricityData.as_view(), name="get_mean"),
]
