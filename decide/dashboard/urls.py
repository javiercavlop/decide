from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_pv, name='dashboard_with_pivot'),
    path('data', views.pivot_data, name='pivot_data'),
]