from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('censusgroups/',views.CensusGroupList.as_view(), name='census_group_list'),
    path('censusgroups/<str:group_name>/',views.CensusGroupDetail.as_view(), name='census_group_detail'),
    path('reuse',views.CensusReuse, name="census_reuse")
]
