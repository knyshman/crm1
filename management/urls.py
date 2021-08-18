from django.urls import path
from . import views


urlpatterns = [path('manager/list_by_manager', views.InteractionListByManager.as_view(), name='interaction_by_manager_list'),
               path('interaction_list/', views.InteractionList.as_view(), name='interaction_list'),
               path('interaction/<int:pk>/', views.InteractionDetail.as_view(), name='interaction_detail'),
               path('interaction/create', views.InteractionCreate.as_view(), name='interaction_create'),
               path('interaction/<int:pk>/update', views.InteractionUpdate.as_view(), name='interaction_update'),
               path('interaction/<int:pk>/delete', views.InteractionDelete.as_view(), name='interaction_delete'),
               path('new_keyword', views.KeywordCreate.as_view(), name='keyword_create')
               ]

urlpatterns += [path('manager/detail/', views.ManagerDetail.as_view(), name='manager_detail'),
                path('manager/update', views.ManagerUpdate.as_view(), name='manager_update'),
                ]