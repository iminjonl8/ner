from django.contrib import admin
from .models import (
    Service, Case, ProductCategory, ProductSubcategory,
    Product, ServiceRequest, ProductRequest, Feedback
)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('created_at', 'updated_at')


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('created_at', 'updated_at')


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')


@admin.register(ProductSubcategory)
class ProductSubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at', 'updated_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'subcategory', 'price',
        'is_new', 'is_hit', 'is_on_sale',
        'created_at', 'updated_at'
    )
    list_filter = (
        'subcategory', 'is_new', 'is_hit',
        'is_on_sale', 'created_at', 'updated_at'
    )
    search_fields = ('title',)


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'city', 'created_at', 'processed')
    list_filter = ('processed', 'created_at')


@admin.register(ProductRequest)
class ProductRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'city', 'created_at', 'processed')
    list_filter = ('processed', 'created_at')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    list_filter = ('created_at',)
