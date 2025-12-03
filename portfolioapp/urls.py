from django.urls import path
from . import views

# Remove app_name if it's causing issues, or use it consistently
# app_name = 'portfolioapp'

urlpatterns = [
    # Class-based views
    path('', views.IndexView.as_view(), name='index'),
   path('projects/', views.ProjectsListView.as_view(), name='projects'),
     path('projects/<int:project_id>/', views.ProjectDetailView.as_view(), name='project_detail'),
     path('projects/<int:project_id>/images/', views.manage_project_images, name='manage_project_images'),
    
    # Alternative: Function-based views (use one or the other)
    # path('', views.index, name='index'),
    # path('projects/', views.projects, name='projects'),
    # path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
]