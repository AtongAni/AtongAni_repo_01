
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    CustomerRegisterView, FarmerRegisterView, MeView,
    AdminDashboardView, AllUsersView, AllPostsView, AllCommentsView,
    UserManagementView, SuspendUserView, ReactivateUserView
)

urlpatterns = [
    path("register/customer/", CustomerRegisterView.as_view()),
    path("register/farmer/", FarmerRegisterView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("me/", MeView.as_view()),
    # Admin endpoints
    path("admin/dashboard/", AdminDashboardView.as_view(), name='admin-dashboard'),
    path("admin/users/", AllUsersView.as_view(), name='admin-users'),
    path("admin/posts/", AllPostsView.as_view(), name='admin-posts'),
    path("admin/comments/", AllCommentsView.as_view(), name='admin-comments'),
    path("admin/users-management/", UserManagementView.as_view(), name='user-management'),
    path("admin/users/<int:user_id>/suspend/", SuspendUserView.as_view(), name='suspend-user'),
    path("admin/users/<int:user_id>/reactivate/", ReactivateUserView.as_view(), name='reactivate-user'),]