from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('import/', views.CensusImport.import_excel,name="import_excel"), 
    path('import_json/', views.CensusImport.import_json,name="import_json"),
    path('import_csv/', views.CensusImport.import_csv,name="import_csv"),
    path('censusgroups/',views.CensusGroupCreate.as_view(), name='census_group_list'),
    path('censusgroups/<int:pk>/',views.CensusGroupDetail.as_view(), name='census_group_detail'),
]