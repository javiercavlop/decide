from django.urls import path, include
from . import views


urlpatterns = [
    path('',views.censusList,name="census_list"),
    path('api', views.CensusCreate.as_view(), name='census_create'),
    path('api/<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('censusgroups/',views.CensusGroupCreate.as_view(), name='census_group_list'),
    path('import/', views.import_excel,name="import_excel"),
    path('export/', views.export_excel,name="export_excel"),
    path('censusgroups/<int:pk>/',views.CensusGroupDetail.as_view(), name='census_group_detail'),
    path('reuse',views.censusReuse, name="census_reuse")
]
