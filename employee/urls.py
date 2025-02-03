from django.urls import path, include
from rest_framework.routers import DefaultRouter
from employee.views import (
    UserRegistrationView, UserLoginView, UserProfileView,
    UserChangePasswordView, SendPasswordResetEmailView, UserPasswordResetView,
    DepartmentViewSet, RoleViewSet, DesignationViewSet,
    UserRoleViewSet, UserDepartmentViewSet, UserDesignationViewSet
)

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'designations', DesignationViewSet, basename='designation')
router.register(r'user-roles', UserRoleViewSet, basename='user-role') 
router.register(r'user-departments', UserDepartmentViewSet, basename='user-department') 
router.register(r'user-designations', UserDesignationViewSet, basename='user-designation') 

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('profile/', UserProfileView.as_view(), name="profile"),
    path('changepassword/', UserChangePasswordView.as_view(), name="changepassword"),
    path('send-password-reset-email/', SendPasswordResetEmailView.as_view(), name="send-password-reset-email"),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name="reset-password"),

    # Include router-generated URLs
    path('', include(router.urls)),
]


