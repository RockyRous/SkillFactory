from django_filters import FilterSet
from .models import Product


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class ProductFilter(FilterSet):
    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Product
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            'name': ['icontains'],
            # количество товаров должно быть больше или равно
            'quantity': ['gt'],
            'price': [
                'lt',  # цена должна быть меньше или равна указанной
                'gt',  # цена должна быть больше или равна указанной
            ],
        }
