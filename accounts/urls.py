from knox import views as knox_views
from accounts.views import LoginView, SignupView
from django.urls import path

urlpatterns = [
    path('login/', LoginView.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('signup', SignupView.as_view(), name='SignupView'),
]