from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Visitor, Turnstile, TurnstileLog
from .serializers import VisitorSerializer, TurnstileSerializer, TurnstileLogSerializer


# Visitor ViewSet
class VisitorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# Turnstile ViewSet
class TurnstileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Turnstile.objects.all()
    serializer_class = TurnstileSerializer

# TurnstileLog ViewSet
class TurnstileLogViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TurnstileLog.objects.all()
    serializer_class = TurnstileLogSerializer


