from django.urls import path
from . import views

urlpatterns = [
    path('avg_temp/<latlng>/<filters>/', views.average_temperature, name='average_t'),
]