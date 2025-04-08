from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'cases', CaseViewSet)
router.register(r'products', ProductViewSet)
router.register(r'service-requests', ServiceRequestViewSet)
router.register(r'product-requests', ProductRequestViewSet)
router.register(r'feedbacks', FeedbackViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
