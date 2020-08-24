from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('add/', views.add, name="add"),
    path('edit/<int:id>', views.edit, name="edit"),
    path('add/', views.add, name="add"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    
]