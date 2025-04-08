from rest_framework import serializers
from .models import (
    Case,
    Service,
    ProductCategory,
    ProductSubcategory,
    Product,
    ServiceRequest,
    ProductRequest,
    Feedback
)

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    # Agar related bo‘lsa, read_only=True qilib,
    # CaseSerializer dan foydalanishingiz mumkin
    cases = CaseSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = '__all__'

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'

class ProductSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSubcategory
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = '__all__'

class ProductRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRequest
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
