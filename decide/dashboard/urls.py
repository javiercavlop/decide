from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view, name='dashboard'),

    path('<int:voting_id>/', views.vista, name = "VotingDashboard"),

    path('download/', views.DashBoardFile.write_doc, name="download"),

    path('<int:voting_id>/', views.vista, name = "VotingDashboard")


    ]
