from django.db import models
from django.utils.timezone import now
from employee.models import User  # Importing User from the employee app
import uuid
import qrcode
from io import BytesIO
from django.core.files import File

# Visitor Model
class Visitor(models.Model):
    visitor_id = models.AutoField(primary_key=True)
    visitor_name = models.CharField(max_length=100, null=False)
    visitor_email = models.EmailField(unique=True, null=False)
    visitor_mobile = models.CharField(max_length=15, unique=True, null=False)
    registered_by = models.ForeignKey(
        User,  # Linking to the User model from the employee app
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='registered_visitors'
    )
    employee_name = models.CharField(max_length=255, null=True, blank=True)
    purpose = models.CharField(max_length=255, null=False)
    visit_code = models.CharField(max_length=8, unique=True, null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.visitor_name} ({self.visitor_email})"

    def save(self, *args, **kwargs):
        if not self.visit_code:
            self.visit_code = str(uuid.uuid4())[:8]  # Generate a unique visit_code of size 8
        super().save(*args, **kwargs)
        self.generate_qr_code()

    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr_data = f"ID: {self.visitor_id}, Name: {self.visitor_name}, Mobile: {self.visitor_mobile}, Visit Code: {self.visit_code}"
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        filename = f'qr_code_{self.visitor_id}.png'
        self.qr_code.save(filename, File(buffer), save=False)
        super().save()


# Turnstile Model
class Turnstile(models.Model):
    id = models.AutoField(primary_key=True)
    visitor = models.ForeignKey(
        Visitor,
        on_delete=models.CASCADE,
        related_name='turnstile_entries'
    )
    entry_time = models.DateTimeField(default=now)
    exit_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Turnstile Entry for {self.visitor.visitor_name}"


# Turnstile Log Model
class TurnstileLog(models.Model):
    id = models.AutoField(primary_key=True)
    turnstile = models.ForeignKey(
        Turnstile,
        on_delete=models.CASCADE,
        related_name='turnstile_logs'
    )
    qr_code_scan = models.CharField(max_length=255, null=False)
    status = models.CharField(max_length=50, null=False, choices=[('success', 'Success'), ('denied', 'Denied')])
    scanned_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Log ID {self.id} - {self.status} ({self.scanned_at})"