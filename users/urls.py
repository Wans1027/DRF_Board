from django.urls import path

from users.serializers import LoginSerializer
from .views import LoginView, RegisterView, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/<int:pk>/', ProfileView.as_view()),

]