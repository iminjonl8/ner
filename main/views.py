from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .models import Question, Car

from .models import (
    Case, Service, Product, ServiceRequest, ProductRequest,
    Feedback, ProductCategory, ProductSubcategory, GalleryItem
)
from .serializers import (
    CaseSerializer, ServiceSerializer, ProductSerializer,
    ServiceRequestSerializer, ProductRequestSerializer, FeedbackSerializer
)

# Пагинация
class DefaultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# ViewSets
class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all().order_by('-created_at')
    serializer_class = CaseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'title']
    filterset_fields = ['title']

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().order_by('price')
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']
    filterset_fields = ['price']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('subcategory').order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']
    filterset_fields = ['price', 'is_new', 'is_hit', 'is_on_sale', 'subcategory__category__name']

class ServiceRequestViewSet(viewsets.ModelViewSet):
    queryset = ServiceRequest.objects.all().order_by('-created_at')
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = DefaultPagination

class ProductRequestViewSet(viewsets.ModelViewSet):
    queryset = ProductRequest.objects.all().order_by('-created_at')
    serializer_class = ProductRequestSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = DefaultPagination

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all().order_by('-created_at')
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'message']
    ordering_fields = ['created_at']
    filterset_fields = ['email', 'phone']

# Views для сайта
def index_view(request):
    products = Product.objects.all().order_by('-created_at')[:4]
    services = Service.objects.all().order_by('price')[:4]
    cases = Case.objects.all().order_by('-created_at')[:6]
    context = {
        'products': products,
        'services': services,
        'cases': cases,
    }
    return render(request, 'main/index.html', context)

def service_view(request):
    services = Service.objects.all().order_by('-created_at')
    return render(request, 'main/service.html', {'services': services})


def car_detail_view(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'main/car_detail.html', {'car': car})






def gallery_view(request):
    items = GalleryItem.objects.select_related('service').all().order_by('-created_at')
    products = Product.objects.all().order_by('-created_at')[:4]
    return render(request, 'main/galary.html', {'items': items})




def category_view(request):
    query = Q()
    category_id = request.GET.get('category')
    if category_id and category_id != 'all':
        query &= Q(subcategory__category__id=category_id)
    min_price = request.GET.get('min')
    max_price = request.GET.get('max')
    if min_price and max_price:
        query &= Q(price__gte=min_price) & Q(price__lte=max_price)
    if request.GET.get('is_new') == 'on':
        query &= Q(is_new=True)
    if request.GET.get('is_hit') == 'on':
        query &= Q(is_hit=True)
    if request.GET.get('is_on_sale') == 'on':
        query &= Q(is_on_sale=True)
    products = Product.objects.filter(query)
    categories = ProductCategory.objects.all()
    return render(request, 'main/category.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
    })

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
   

    # Похожие из той же подкатегории
    similar_products = Product.objects.filter(subcategory=product.subcategory).exclude(pk=pk)
    similar_count = similar_products.count()

    if similar_count >= 4:
        products = similar_products[:4]
    else:
        # Добавляем других товаров, чтобы довести до 4
        extra_needed = 4 - similar_count
        others = Product.objects.exclude(pk__in=similar_products.values_list('pk', flat=True)).exclude(pk=pk)[:extra_needed]
        products = list(similar_products) + list(others)

    return render(request, 'main/product_detail.html', {
        'product': product,
        'products': products
    })


@csrf_exempt  
def send_question(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        # тут можно отправить в телегу, сохранить в БД и т.д.
        print(f"Имя: {name}, Телефон: {phone}")  # временно в консоль

        return redirect('index')  # или куда хочешь
    return redirect('index')

def error_404_view(request, exception):
    return render(request, 'main/404.html', status=404)

def error_505_view(request):
    return render(request, 'main/505.html', status=500)
