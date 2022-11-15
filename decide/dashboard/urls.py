from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('<int:voting_id>/', views.vista, name = "VotingDashboard")
    ]
