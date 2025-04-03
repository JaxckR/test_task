from django.db import models
from django.urls import reverse


class Order(models.Model):
    """
    Модель заказа

    Атрибуты:
    table_number: int - Номер столика
    items: dict - Список заказанных блюд
    total_price: float - Общая стоимость. Вычисляется в методе save
    status: str - Статус заказа. Принимает значения из STATUS_CHOICES
    date_created - Дата создания
    time_updated - Дата обновления

    Методы:
    get_absolute_url - получение url страницы информации о заказе
    __str__ - отображение названия записи
    get_items - получение значений для отображения в html
    """
    STATUS_CHOICES = [
        ('В ожидании', 'В ожидании'),
        ('Готово', 'Готово'),
        ('Оплачено', 'Оплачено')
    ]
    table_number = models.IntegerField(verbose_name='Номер столика')
    items = models.JSONField(verbose_name='Список заказанных блюд')
    total_price = models.FloatField(verbose_name='Общая цена')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='В ожидании', verbose_name='Статус')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def get_items(self):
        return ", ".join([f"{v} - {price}" for v, price in self.items.items()])

    def __str__(self):
        return f"{self.table_number} - {self.status}"

    def get_absolute_url(self):
        return reverse('detail', kwargs={'order_id': self.pk})

    def save(self, *args, **kwargs):
        self.total_price = sum(float(item) for item in self.items.values())
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_created']
