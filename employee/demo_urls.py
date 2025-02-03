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

# Add custom routes for non-ViewSet views using the router
router.register(r'register', UserRegistrationView, basename='register')
router.register(r'login', UserLoginView, basename='login')
router.register(r'profile', UserProfileView, basename='profile')
router.register(r'changepassword', UserChangePasswordView, basename='changepassword')
router.register(r'send-password-reset-email', SendPasswordResetEmailView, basename='send-password-reset-email')
router.register(r'reset-password/(?P<uid>[^/.]+)/(?P<token>[^/.]+)', UserPasswordResetView, basename='reset-password')

# The router now contains all the URL routes
urlpatterns = [
    path('', include(router.urls)),
]

