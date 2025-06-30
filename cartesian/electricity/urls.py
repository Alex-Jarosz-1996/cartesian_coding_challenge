from django.urls import path

from .views import GetElectricityData

urlpatterns = [path("get", GetElectricityData.as_view(), name="get_data")]
