from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('import/', views.import_excel,name="import_excel"),
<<<<<<< HEAD
=======
    path('import_json/', views.import_json,name="import_json"),
    path('import_csv/', views.import_csv,name="import_csv"),
>>>>>>> ffdaec2f5671f6a9f755a0922ed07bf1461ccc97
    path('export/', views.export_excel,name="export_excel"),
    path('censusgroups/',views.CensusGroupCreate.as_view(), name='census_group_list'),
    path('censusgroups/<int:pk>/',views.CensusGroupDetail.as_view(), name='census_group_detail'),
    
]

