from rest_framework import serializers
from employee.models import User
from .models import Department, Role, Designation
from .models import UserRole, UserDepartment, UserDesignation
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from employee.utils import Util


### User Registration Serializer ###
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'mobile', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'error': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)  # Remove password2
        return User.objects.create_user(**validated_data)


### User Login Serializer ###
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)


### User Profile Serializer ###
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'mobile']


### User Change Password Serializer ###
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"error": "Passwords do not match."})
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


### Send Password Reset Email Serializer ###
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate(self, attrs):
        email = attrs.get("email")
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "This email is not registered."})

        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))  # Using `pk` instead of `id`
        token = PasswordResetTokenGenerator().make_token(user)
        reset_link = f'http://localhost:3000/api/reset/{uid}/{token}'

        # For debugging purposes
        print("Password Reset Link:", reset_link)

        return attrs


### User Password Reset Serializer ###
class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        try:
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError({"error": "Passwords do not match."})

            uid = self.context.get('uid')
            token = self.context.get('token')

            id = smart_str(urlsafe_base64_decode(uid))  # Decode UID safely
            user = User.objects.get(pk=id)  # Use `pk` instead of `id`

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError({"error": "Invalid or expired token."})

            user.set_password(attrs['password'])
            user.save()
            return attrs

        except (DjangoUnicodeDecodeError, ValueError):
            raise serializers.ValidationError({"error": "Invalid UID encoding."})


### Department Serializer ###
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['dept_id', 'department_name']


### Role Serializer ###
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role_id', 'role_name']


### Designation Serializer ###
class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ['desgn_id', 'designation_name']



### UserRole Serializer
class UserRoleSerializer(serializers.ModelSerializer):
    emp_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user')
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), source='role')

    class Meta:
        model = UserRole
        fields = ['id', 'emp_id', 'role_id']


### UserDepartment Serializer
class UserDepartmentSerializer(serializers.ModelSerializer):
    emp_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user')
    dept_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), source='department')

    class Meta:
        model = UserDepartment
        fields = ['id', 'emp_id', 'dept_id']


### UserDesignation Serializer
class UserDesignationSerializer(serializers.ModelSerializer):
    emp_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user')
    desgn_id = serializers.PrimaryKeyRelatedField(queryset=Designation.objects.all(), source='designation')

    class Meta:
        model = UserDesignation
        fields = ['id', 'emp_id', 'desgn_id']

