from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from api.pagination import OrderPagination
from api.serializers import OrderSerializer
from cafe.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Order

    Доступные endpoints:
    - 'GET /api/v1/orders/' - получить список всех заказов
    - 'POST /api/v1/orders/' - создать новый заказ
    - 'GET /api/v1/orders/{id}/' - получить информацию о заказе
    - 'PATCH /api/v1/orders/{id}/' - частично обновить сведения о заказе
    - 'PUT /api/v1/orders/{id}/' - полностью обновить сведения о заказе
    - 'DELETE /api/v1/orders/{id}/' - удалить сведения о заказе
    - 'GET /api/v1/orders/{id}/items/' - получить информацию о позициях заказа
    - 'PATCH /api/v1/orders/{id}/items/' - изменить информацию о позициях заказа

    Поиск происходит с помощь query параметра q в классе SearchFilter по значениям
    table_number или status.
    Используемый сериализатор - OrderSerializer
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    search_fields = ['table_number', 'status']
    filter_backends = [SearchFilter]

    @action(methods=['GET', 'PATCH'], detail=True)
    def items(self, request, pk=None):
        if request.method == 'GET':
            items = Order.objects.all().values_list('table_number', 'items')
            try:
                return Response(items.get(pk=pk)[-1])
            except ObjectDoesNotExist:
                return Response({"error": "Данная запись отсутствует"})
        elif request.method == 'PATCH':
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data.get('items'))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
