from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from portfolio.models import Portfolio
from .serializers import PortfolioSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class PortfolioViewSet(viewsets.ModelViewSet):
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Portfolio.objects.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
