from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CategoryViewSet, UserRegistrationView, get_user_by_id
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('users/<int:user_id>/', get_user_by_id, name='get_user_by_id'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
