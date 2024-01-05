from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('summary/', views.summary, name='summary'),
    path('signout/', views.signout, name='signout'),
    path('api/register/', views.UserRegistrationAPIView.as_view(), name='register'),
    # path('api/login/', views.UserLoginAPIView.as_view(), name='login'),
    # path('api/logout/', views.UserLogoutAPIView.as_view(), name='logout'),
]
