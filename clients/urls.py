from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('clients/', views.client_list, name='client_list'),
    path('clients/add/', views.client_add, name='client_add'),
    path('clients/<int:pk>/', views.client_detail, name='client_detail'),
    path('clients/<int:pk>/edit/', views.client_edit, name='client_edit'),
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),
    path('clients/<int:pk>/notes/', views.client_notes, name='client_notes'),
    path('clients/<int:pk>/history/', views.client_history, name='client_history'),
    path('monitoring/', views.monitoring, name='monitoring'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]