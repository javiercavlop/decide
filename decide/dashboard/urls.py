from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('download/', views.DashBoardFile.write_doc, name="download"),
]