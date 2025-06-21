from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from portfolio.models import Portfolio, Holding, DailySummary
from .serializers import PortfolioSerializer, HoldingSerializer, DailySummarySerializer
from rest_framework.exceptions import PermissionDenied


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

class HoldingViewSet(viewsets.ModelViewSet):
    serializer_class = HoldingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Holding.objects.filter(portfolio__user=self.request.user)

    def perform_create(self, serializer):
        portfolio = serializer.validated_data['portfolio']
        if portfolio.user != self.request.user:
            raise PermissionDenied("You can't add holdings to someone else's portfolio")
        serializer.save()

class DailySummaryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DailySummarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DailySummary.objects.filter(holding__portfolio__user = self.request.user).order_by('-date')