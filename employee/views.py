from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from employee.serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, 
    UserChangePasswordSerializer, SendPasswordResetEmailSerializer, 
    UserPasswordResetSerializer, DepartmentSerializer, RoleSerializer, 
    DesignationSerializer,
    UserRoleSerializer, 
    UserDesignationSerializer,
    UserDepartmentSerializer
)
from .models import (
    User, Department, Role, Designation,
    UserRole, UserDepartment, UserDesignation)


# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


### User Registration ###
class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'data': serializer.data, 'message': 'Registration Successful.'}, 
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


### User Login ###
class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            try:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    raise ValueError("Invalid password")
            except User.DoesNotExist:
                return Response({"error": "Invalid email or password."}, status=status.HTTP_404_NOT_FOUND)

            token = get_tokens_for_user(user)
            return Response({'token': token, 'message': 'Login Successful.'}, status=status.HTTP_200_OK)


### User Profile ###
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


### Change Password ###
class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = UserChangePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.update(user, serializer.validated_data)
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


### Send Password Reset Email ###
class SendPasswordResetEmailView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Password reset mail sent successfully"}, status=status.HTTP_200_OK)


### Password Reset ###
class UserPasswordResetView(APIView):
    def post(self, request, *args, **kwargs):
        uid = kwargs.get('uid')
        token = kwargs.get('token')

        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)

        return Response({'message': "Password reset successful."}, status=status.HTTP_200_OK)


### Department ViewSet ###
class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


### Role ViewSet ###
class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


### Designation ViewSet ###
class DesignationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer

### UserRole ViewSet
class UserRoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if the user-role combination already exists
        user = serializer.validated_data['user']
        role = serializer.validated_data['role']
        if UserRole.objects.filter(user=user, role=role).exists():
            return Response(
                {"error": "This user already has this role."},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Check if the updated user-role combination already exists
        user = serializer.validated_data.get('user', instance.user)
        role = serializer.validated_data.get('role', instance.role)
        if UserRole.objects.filter(user=user, role=role).exclude(id=instance.id).exists():
            return Response(
                {"error": "This user-role combination already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "User role deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

### UserDepartment ViewSet
class UserDepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserDepartment.objects.all()
    serializer_class = UserDepartmentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if the user-department combination already exists
        user = serializer.validated_data['user']
        department = serializer.validated_data['department']
        if UserDepartment.objects.filter(user=user, department=department).exists():
            return Response(
                {"error": "This user already belongs to this department."},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Check if the updated user-department combination already exists
        user = serializer.validated_data.get('user', instance.user)
        department = serializer.validated_data.get('department', instance.department)
        if UserDepartment.objects.filter(user=user, department=department).exclude(id=instance.id).exists():
            return Response(
                {"error": "This user-department combination already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "User department entry deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

### UserDesignation ViewSet : need update
class UserDesignationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserDesignation.objects.all()
    serializer_class = UserDesignationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if the user-designation combination already exists
        user = serializer.validated_data['user']
        designation = serializer.validated_data['designation']
        if UserDesignation.objects.filter(user=user, designation=designation).exists():
            return Response(
                {"error": "This user already has this designation."},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Check if the updated user-designation combination already exists
        user = serializer.validated_data.get('user', instance.user)
        designation = serializer.validated_data.get('designation', instance.designation)
        if UserDesignation.objects.filter(user=user, designation=designation).exclude(id=instance.id).exists():
            return Response(
                {"error": "This user-designation combination already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "User designation entry deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

