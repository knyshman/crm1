from django.urls import path
from . import views


urlpatterns = [
    path('', views.CompanyListView.as_view(), name='company_list'),
    path('<int:pk>', views.CompanyDetailView.as_view(), name='company_detail'),
    path('create', views.CompanyCreateView.as_view(), name='company_create'),
    path('<int:pk>/update/', views.CompanyUpdateView.as_view(), name='company_update'),
    path('<int:pk>/delete/', views.CompanyDeleteView.as_view(), name='company_delete'),

]
urlpatterns += [path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),
                path('project/create', views.ProjectCreateView.as_view(), name='project_create'),
                path('project/<int:pk>/update', views.ProjectUpdateView.as_view(), name='project_update'),
                path('project/<int:pk>/delete', views.ProjectDeleteView.as_view(), name='project_delete'),
                path('projects', views.ProjectListView.as_view(), name='project_list'),
                path('<int:pk>/company_interactions', views.InteractionByCompanyList.as_view(), name='interaction_by_company'),
                path('<int:pk>/project_interactions', views.InteractionByProjectList.as_view(), name='interaction_by_project')

]