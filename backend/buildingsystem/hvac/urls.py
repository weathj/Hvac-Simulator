from django.urls import path
from . import api_views

urlpatterns = [
    path('api/create/', api_views.CreateView.as_view(), name='create'),
    path('api/<uuid:session_id>/airunit/', api_views.AirUnitValuesView.as_view(), name='airunit-values'),
    path('api/<uuid:session_id>/zone/<int:pk>/', api_views.ZoneValuesView.as_view(), name='zone-values'),
    path('api/<uuid:session_id>/zones/', api_views.AllZoneValuesView.as_view(), name='all-zones-values'),
    path('api/<uuid:session_id>/air/', api_views.AirValuesView.as_view(), name='air-values'),
    path('api/<uuid:session_id>/delete/', api_views.DeleteView.as_view(), name='delete')
]