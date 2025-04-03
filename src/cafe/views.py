from django.db.models import Q, Sum
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from cafe.forms import CreateOrderForm, UpdateOrderForm
from cafe.models import Order
from cafe.utils import DataMixin


class HomeView(DataMixin, ListView):
    """
    Представление главной страницы

    Записи отображаются в шаблоне home.html,
    имеют пагинацию по 4 записи на страницу.
    Список записей передается в шаблон под названием orders
    """
    title_page = 'Главная'
    template_name = 'cafe/home.html'
    model = Order
    context_object_name = 'orders'
    paginate_by = 4


class TotalView(DataMixin, ListView):
    """
    Представление страницы с общей выручкой

    Используется шаблон главной страницы с проверкой
    на наличие значения total_price. Записи имеют
    пагинацию по 3 на страницу
    """
    title_page = "Общая выручка"
    model = Order
    template_name = 'cafe/home.html'
    context_object_name = 'orders'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total = self.get_queryset().aggregate(Sum('total_price'))['total_price__sum']
        context['total_price'] = total if total else 0
        return context

    def get_queryset(self):
        return Order.objects.filter(status='Оплачено')


class SearchView(DataMixin, ListView):
    """
    Представление логики обработки поиска

    Поиск происходит по фильтрам iregex.
    Используется шаблон home.html с query параметром.
    Пагинация по 4 записи на страницу
    """
    title_page = 'Поиск'
    model = Order
    template_name = 'cafe/home.html'
    context_object_name = 'orders'
    paginate_by = 4

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Order.objects.filter(Q(table_number__iregex=query) | Q(status__iregex=query))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


class DetailOrderView(DataMixin, UpdateView):
    """
    Представление детального обзора записей

    Отображает id, table_number, items, total_price и status заказа
    по pk. Также позволяет обновлять status и удалять заказ.
    После удаления происходит переадресация на главную страницу сайта.
    Использует форму UpdateOrderForm для обновления статуса заказа
    """
    title_page = 'Информация о заказе'
    model = Order
    form_class = UpdateOrderForm
    template_name = 'cafe/detail.html'
    pk_url_kwarg = 'order_id'
    context_object_name = 'order'
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            Order.objects.get(pk=self.kwargs['order_id']).delete()
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)


class CreateOrder(DataMixin, CreateView):
    """
    Представление создания записи заказа

    Использует форму CreateOrderForm.
    Форма отображается в шаблоне create.html. После успешного создания
    происходит переадресация на главную страницу сайта
    """
    title_page = 'Создание заказа'
    form_class = CreateOrderForm
    template_name = 'cafe/create.html'
    success_url = reverse_lazy('home')
