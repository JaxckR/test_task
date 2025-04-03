from django import forms
from re import match

from .models import Order


class CreateOrderForm(forms.ModelForm):
    """
    Форма создания записи заказа

    Отображаемые поля - table_number, items.
    В методе clean_items происходит логика обработки и валидации данных
    items в соответствии с value price
    """
    items = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Блюдо цена\nЦезарь 450'}),
        label='Список заказанных блюд')

    class Meta:
        model = Order
        fields = ['table_number', 'items']
        widgets = {
            'table_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_items(self):
        items = self.cleaned_data['items']
        items = items.split('\r\n')
        items = [item.split(' ') for item in items]

        for item in items:
            if len(item) != 2:
                self.add_error('items', 'Введите позиции согласно примеру')
            elif not bool(match(r'^\d+([.,]\d+)?$', item[-1])):
                self.add_error('items', 'Значение должно быть положительным числом')

        result = {item[0]: item[-1].replace(',', '.') for item in items}
        return result


class UpdateOrderForm(forms.ModelForm):
    """
    Форма обновления статуса заказа

    Отображаемые поля - status
    """
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
