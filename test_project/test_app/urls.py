from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup,name='signup'),
    path('accounts/login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('summary/', views.summary, name='summary'),
    path('signout/', views.signout, name='signout'),
]