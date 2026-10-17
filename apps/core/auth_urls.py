from django.urls import path
from .auth_views import CurrentUserView, LoginView, RegistrationView, logout

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth-login'),
    path('register/', RegistrationView.as_view(), name='auth-register'),
    path('logout/', logout, name='auth-logout'),
    path('me/', CurrentUserView.as_view(), name='auth-me'),
]
