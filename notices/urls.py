from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'), # Homepage
    path('notice/<int:pk>/', views.notice_detail, name='notice_detail'), 
    path('login/', auth_views.LoginView.as_view(template_name='staff/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('dashboard/create/', views.create_notice, name='create_notice'),
    path('dashboard/delete/<int:pk>/', views.delete_notice, name='delete_notice'),
    path('dashboard/edit/<int:pk>/', views.edit_notice, name='edit_notice'),
    path('view/<int:notice_id>/<str:file_type>/', views.file_viewer, name='view_main'),
path('view/<int:notice_id>/<str:file_type>/<int:file_id>/', views.file_viewer, name='view_sub'),
]