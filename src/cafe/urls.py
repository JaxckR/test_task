from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('detail/<int:order_id>/', views.DetailOrderView.as_view(), name='detail'),
    path('total/', views.TotalView.as_view(), name='total'),
    path('neworder/', views.CreateOrder.as_view(), name='create'),
    path('search/', views.SearchView.as_view(), name='search'),
]