from django.contrib.auth.models import User
from rest_framework import serializers
from portfolio.models import Portfolio, Holding, DailySummary


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['id', 'name']

class HoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holding
        fields = ['id', 'ticker', 'quantity', 'portfolio']

class DailySummarySerializer(serializers.ModelSerializer):
    holding = serializers.StringRelatedField()

    class Meta:
        model = DailySummary
        fields = ['id', 'holding', 'data', 'open_price', 'close_price', 'high_price', 'low_price', 'total_value']
