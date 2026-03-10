from django.urls import path
from . import api_views

urlpatterns = [
    path('api/create/', api_views.CreateView.as_view(), name='create'),
    path('api/airunit/', api_views.AirUnitValuesView.as_view(), name='airunit-values'),
    path('api/zone/<int:pk>/', api_views.ZoneValuesView.as_view(), name='zone-values'),
    path('api/zones/', api_views.AllZoneValuesView.as_view(), name='all-zones-values'),
    path('api/air/', api_views.AirValuesView.as_view(), name='air-values')
]