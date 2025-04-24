from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import index_view, service_view, gallery_view, category_view, product_detail_view, send_question, car_detail_view, send_form



from .views import (
    index_view,
    service_view,
    gallery_view,
    category_view,
    product_detail_view,
    send_question,
)

urlpatterns = [
    path('', index_view, name='index'),
    path('services/', service_view, name='services'),
    path('send-form/', send_form, name='send_form'),
    path('gallery/', gallery_view, name='gallery'),
    path('category/', category_view, name='category'),
    # path('car/<int:pk>/', car_detail_view, name='car_detail'),
    path('product/<int:pk>/', product_detail_view, name='product_detail'),
    path('send-question/', send_question, name='send_question'),
    path('shop/', category_view, name='shop'),
    
]
