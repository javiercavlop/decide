from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('import_csv/', views.CensusImport.import_csv,name="import_csv"),
    path('censusgroups/',views.CensusGroupCreate.as_view(), name='census_group_list'),
    path('censusgroups/<int:pk>/',views.CensusGroupDetail.as_view(), name='census_group_detail'),
]