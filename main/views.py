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
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json, requests
from django.conf import settings
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

@csrf_exempt  # или @csrf_protect + ставишь CSRF в заголовке X-CSRFToken
def send_form(request):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Только POST'}, status=405)

    try:
        # 1) Парсим JSON
        data = json.loads(request.body.decode('utf-8'))
        name    = data.get('name', '—')
        phone   = data.get('phone', '—')
        city    = data.get('city', 'не указан')
        comment = data.get('comment', '—')
        product = data.get('product', 'Без товара')

        # 2) Формируем сообщение
        message = (
            f"📝 <b>Новая заявка с сайта</b>\n"
            f"📦 <b>Товар:</b> {product}\n"
            f"👤 <b>Имя:</b> {name}\n"
            f"📞 <b>Телефон:</b> {phone}\n"
            f"🏙️ <b>Город:</b> {city}\n"
            f"💬 <b>Комментарий:</b> {comment}"
        )

        # 3) Шлём в Telegram
        resp = requests.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                'chat_id':   settings.TELEGRAM_CHAT_ID,
                'text':      message,
                'parse_mode': 'HTML'
            },
            timeout=5
        )
        resp.raise_for_status()

        return JsonResponse({'ok': True})

    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)
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
    gallery_items = GalleryItem.objects.all().order_by('-created_at')[:4]
    context = {
        'products': products,
        'services': services,
        'cases': cases,
        'items': gallery_items,
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

    # Subkategoriya bo‘yicha filter
    subcategory_id = request.GET.get('subcategory')
    if subcategory_id:
        query &= Q(subcategory__id=subcategory_id)

    # (Avvalgi filtrlar qoladi)
    min_price = request.GET.get('min')
    max_price = request.GET.get('max')
    if min_price:
        query &= Q(price__gte=min_price)
    if max_price:
        query &= Q(price__lte=max_price)

    if request.GET.get('is_new') == 'on':
        query &= Q(is_new=True)
    if request.GET.get('is_hit') == 'on':
        query &= Q(is_hit=True)
    if request.GET.get('is_on_sale') == 'on':
        query &= Q(is_on_sale=True)

    products = Product.objects.filter(query)
    categories = ProductCategory.objects.prefetch_related('subcategories')

    return render(request, 'main/category.html', {
        'products': products,
        'categories': categories,
        'selected_subcategory': subcategory_id,
    })



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
