from rest_framework.pagination import PageNumberPagination


class OrderPagination(PageNumberPagination):
    """
    Класс пагинации для списка заказов

    Можно самостоятельно изменить количество отображаемых
    записей с помощью query параметра page_size. Максимальное
    количество отображаемых записей в одном запросе 1000
    """
    page_size = 100
    max_page_size = 1000
    page_size_query_param = 'page_size'