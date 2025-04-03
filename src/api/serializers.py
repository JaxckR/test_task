from rest_framework import serializers

from cafe.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Order

    Отображаемые значения указаны в field классе Meta
    В методе validate происходит проверка на обязательность
    полей required при создании записи

    В методе validate_items происходит проверка, что
    items является словарем и значения являются числовыми либо
    вещественными

    В методе validate_status происходит проверка, чтобы
    значение status не изменялось при создании объекта
    """
    id = serializers.IntegerField(read_only=True)
    table_number = serializers.IntegerField(required=False)
    items = serializers.JSONField(required=False)
    total_price = serializers.FloatField(read_only=True)
    status = serializers.CharField(required=False)
    date_created = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'table_number', 'items', 'total_price', 'status', 'date_created']

    def validate(self, data):
        required = ['items', 'table_number']
        if self.instance is None:
            if data == {}:
                raise serializers.ValidationError({field: "Это обязательное поле" for field in required})

            for field in required:
                if field not in data:
                    raise serializers.ValidationError({field: "Это обязательное поле"})

        return data

    def validate_items(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError('Значение должно быть в формате словаря')

        for item in value.values():
            if not isinstance(item, int) and not isinstance(item, float):
                raise serializers.ValidationError('Значения должны быть числами')

        return value

    def validate_status(self, value):
        if self.instance is None:
            raise serializers.ValidationError('Поле status можно менять только после создания объекта')
        return value
