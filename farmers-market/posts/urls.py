from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, PostCommentViewSet, FarmerHarvestProfileViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'farmer-harvest-profile', FarmerHarvestProfileViewSet, basename='farmer-harvest-profile')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/comments/', PostCommentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='post-comments-list'),
    path('posts/<int:post_id>/comments/<int:pk>/', PostCommentViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='post-comments-detail'),
]
