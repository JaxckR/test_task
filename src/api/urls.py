from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'orders', views.OrderViewSet, basename='orders')


urlpatterns = [
    path('', include(router.urls)),
]