from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator


# UserManager to manage User creation
class UserManager(BaseUserManager):
    def create_user(self, name, email, mobile, password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        
        user = self.model(
            name=name,
            email=self.normalize_email(email),
            mobile=mobile
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, mobile, password=None):
        user = self.create_user(
            name=name,
            email=email,
            mobile=mobile,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


# Custom User model
class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    mobile = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid mobile number")]
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name', 'mobile']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin or self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_admin or self.is_superuser


# Department model
class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.department_name


# Role model
class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.role_name


# Designation model
class Designation(models.Model):
    desgn_id = models.AutoField(primary_key=True)
    designation_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.designation_name


# User_Role Table (Relationship between User and Role)
class UserRole(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)  # Changed from emp_id to user
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'role'], name='unique_user_role')  # Updated field names for clarity
        ]

    def __str__(self):
        return f"{self.user.name} - {self.role.role_name}"


# User_Department Table (Relationship between User and Department)
class UserDepartment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)  # Changed from emp_id to user
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'department'], name='unique_user_department')  # Updated field names for clarity
        ]

    def __str__(self):
        return f"{self.user.name} - {self.department.department_name}"


# User_Designation Table (Relationship between User and Designation)
class UserDesignation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)  # Changed from emp_id to user
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'designation'], name='unique_user_designation')  # Updated field names for clarity
        ]

    def __str__(self):
        return f"{self.user.name} - {self.designation.designation_name}"
