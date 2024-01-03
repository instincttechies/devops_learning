from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/signup/', views.signup,name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('summary/', views.summary, name='summary'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='login'),
]