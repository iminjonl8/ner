from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta

from .models import (
    Question, Car, Category,
    Case, Service, Product, ServiceRequest, ProductRequest,
    Feedback, ProductCategory, ProductSubcategory, GalleryItem
)
from .serializers import (
    CaseSerializer, ServiceSerializer, ProductSerializer,
    ServiceRequestSerializer, ProductRequestSerializer, FeedbackSerializer
)

import requests
from django.http import HttpResponse

BOT_TOKEN = '7558537687:AAGVPTcTPk1LYyzrnVTbSRj4TUsRkIBmBXQ'
CHAT_ID = '6349387390'

from django.conf import settings
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def send_form(request):
    if request.method == "POST":
        name = request.POST.get('name', '—')
        phone = request.POST.get('phone', '—')
        city = request.POST.get('city', 'не указан')
        comment = request.POST.get('comment', '—')

        message = f"""📝 <b>Новая заявка с сайта</b>
👤 Имя: {name}
📞 Телефон: {phone}
🏙️ Город: {city}
💬 Комментарий: {comment}"""

        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": settings.TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }

        try:
            response = requests.post(url, json=payload)
            print("Статус код Telegram:", response.status_code)  # <-- Логирование
            print("Ответ Telegram:", response.text)
            response.raise_for_status()  
            return HttpResponse("Заявка отправлена!")
        except Exception as e:
            return HttpResponse(f"Ошибка: {str(e)}", status=500)

    return HttpResponse("Method not allowed", status=405)

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
    return render(request, 'main/product_detail.html', {'car': car})


def sidebar_categories_view(request):
    categories = ProductCategory.objects.prefetch_related('subcategories').all()
    return render(request, 'main/sidebar_categories.html', {'categories': categories})


def gallery_view(request):
    items = GalleryItem.objects.select_related('service').all().order_by('-created_at')
    products = Product.objects.all().order_by('-created_at')[:4]
    return render(request, 'main/galary.html', {'items': items})


def category_view(request):
    query = Q()
    now = timezone.now()
    # Автоматическое снятие статуса "Новинка" через 30 дней
    month_ago = now - timedelta(days=30)
    Product.objects.filter(
        is_new=True,
        created_at__lt=month_ago
    ).update(is_new=False)

    # Фильтр по категории
    category_id = request.GET.get('category')
    if category_id and category_id != 'all':
        query &= Q(subcategory__category__id=category_id)

    # Фильтр по цене
    min_price = request.GET.get('min')
    max_price = request.GET.get('max')
    try:
        if min_price:
            query &= Q(price__gte=float(min_price))
        if max_price:
            query &= Q(price__lte=float(max_price))
    except (TypeError, ValueError):
        pass

    # Приоритетная фильтрация
    if request.GET.get('is_new') == 'on':
        query &= Q(is_new=True)
    if request.GET.get('is_hit') == 'on':
        query &= Q(is_hit=True)
    if request.GET.get('is_on_sale') == 'on':
        query &= Q(is_on_sale=True)

    products = Product.objects.filter(query)
    categories = ProductCategory.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'request': request,
    }
    return render(request, 'main/category.html', context)


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    similar_products = Product.objects.filter(subcategory=product.subcategory).exclude(pk=pk)
    similar_count = similar_products.count()
    car = Car.objects.first()
    if similar_count >= 4:
        products = similar_products[:4]
    else:
        extra_needed = 4 - similar_count
        others = Product.objects.exclude(pk__in=similar_products.values_list('pk', flat=True)).exclude(pk=pk)[:extra_needed]
        products = list(similar_products) + list(others)
    return render(request, 'main/product_detail.html', {
        'product': product,
        'car': car,
        'products': products
    })


@csrf_exempt
def send_question(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        print(f"Имя: {name}, Телефон: {phone}")
        return redirect('index')
    return redirect('index')


def error_404_view(request, exception):
    return render(request, 'main/404.html', status=404)


def error_505_view(request):
    return render(request, 'main/505.html', status=500)


def shop_view(request):
    categories = Category.objects.prefetch_related('subcategories').all()
    return render(request, 'shop.html', {'categories': categories})
