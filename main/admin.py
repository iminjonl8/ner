from django.contrib import admin
from django.utils.html import format_html
from .models import Car
from .models import (
    Service, Case, ProductCategory, ProductSubcategory,
    Product, ProductImage, ServiceRequest, ProductRequest, Feedback, GalleryItem
)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'subcategory', 'price', 'image_tag', 'created_at', 'updated_at')
    list_display_links = ('title',)
    list_filter = (
        'subcategory', 'is_new', 'is_hit',
        'is_on_sale', 'created_at', 'updated_at'
    )
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    inlines = [ProductImageInline]

    def image_tag(self, obj):
        if obj.image1:
            return format_html('<img src="{}" width="50" />', obj.image1.url)
        return "-"
    image_tag.short_description = 'Изображение'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'updated_at')
    list_display_links = ('title',)
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'updated_at', 'price')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    list_display_links = ('title',)
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    list_display_links = ('name',)
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('name',)

@admin.register(ProductSubcategory)
class ProductSubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at', 'updated_at')
    list_display_links = ('name',)
    list_filter = ('category', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('category', 'name',)

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'city', 'created_at', 'processed')
    list_filter = ('processed', 'created_at')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_editable = ('processed',)

@admin.register(ProductRequest)
class ProductRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'city', 'created_at', 'processed')
    list_filter = ('processed', 'created_at')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_editable = ('processed',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'type')
    search_fields = ('name',)
   
    def car_type_display(self, obj):
        return obj.type
    car_type_display.short_description = "Тип автомобиля"