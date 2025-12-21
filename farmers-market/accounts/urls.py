
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomerRegisterView, FarmerRegisterView, MeView

urlpatterns = [
    path("register/customer/", CustomerRegisterView.as_view()),
    path("register/farmer/", FarmerRegisterView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("me/", MeView.as_view()),
]
