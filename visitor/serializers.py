from rest_framework import serializers
from .models import Visitor, Turnstile, TurnstileLog


# Visitor Serializer
class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = [
            'visitor_id', 'visitor_name', 'visitor_email', 'visitor_mobile', 'registered_by', 
            'employee_name', 'visit_code', 'qr_code', 'created_at', 'updated_at'
        ]
        read_only_fields = ['visitor_id', 'visit_code', 'qr_code', 'created_at', 'updated_at']

# Turnstile Serializer
class TurnstileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turnstile
        fields = ['id', 'visitor', 'entry_time', 'exit_time']
        read_only_fields = ['id', 'entry_time']

# Turnstile Log Serializer
class TurnstileLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurnstileLog
        fields = ['id', 'turnstile', 'qr_code_scan', 'status', 'scanned_at']
        read_only_fields = ['id', 'scanned_at']