from django.urls import path
from . import views

urlpatterns = [

    path('', views.main_page, name='dashboard'),

    path('dashboard', views.DashboardView.as_view, name='dashboard'),

    path('dashboard/<int:voting_id>/', views.vista, name = "VotingDashboard"),

    path('download/', views.DashBoardFile.write_doc, name="download"),



    ]
