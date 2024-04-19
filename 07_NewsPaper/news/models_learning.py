from datetime import datetime

from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)


director = 'DI'
admin = 'AD'
cook = 'CO'
cashier = 'CA'
cleaner = 'CL'

POSITIONS = [
    (director, 'Директор'),
    (admin, 'Администратор'),
    (cook, 'Повар'),
    (cashier, 'Кассир'),
    (cleaner, 'Уборщик')
]


class Staff(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=2,
                                choices=POSITIONS,
                                default=cashier)
    labor_contract = models.IntegerField()

    def get_last_name(self):
        return self.full_name.split()[0]


class Order(models.Model):  # наследуемся от класса Model
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    pickup = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)  # связь между «Сотрудником» и «Заказом»
    products = models.ManyToManyField(Product, through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:  # если завершён, возвращаем разность объектов
            return (self.time_out - self.time_in).total_seconds()
        else:  # если ещё нет, то сколько длится выполнение
            return (datetime.now() - self.time_in).total_seconds()


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1, db_column='amount')

    def product_sum(self):
        product_price = self.product.price
        return product_price * self.amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()  # Сохраняет изменения в бд


class Example(models.Model):
    # object_id = models.AutoField()  # Целочисленное поле, которое автоматически увеличивается для каждой строки.
    boolean = models.BooleanField(default=False)  # Поле логических переменных — True или False.
    small_string = models.CharField(max_length=64, default="Default value")  # Строковый тип. Используется, как правило, для небольших строковых данных.
    some_data = models.DateField(auto_now_add=True)  # Поле, предназначенное для хранения даты. В Python оно представлено объектом datetime.date.
    some_datetime = models.DateTimeField(auto_now_add=True)  # Класс, представляющий дату и время. В Python представлен объектом datetime.datetime.
    personal_email = models.EmailField()  # Подтип поля CharField, специализированный на хранении электронной почты. Отличие заключается в том, что при сохранении объекта, данные проверяются на соответствие формату anyone@anywhere.com.
    price = models.FloatField(default=0.99)  # Поле для чисел с плавающей точкой.
    count = models.IntegerField(default=0)  # Целочисленное поле. Может принимать значения от -2147483648 до 2147483647.
    article_text = models.TextField()  # Поле, оптимизированное для хранения больших текстов.
    tea_time = models.TimeField()  # Поле, аналогичное DateField и DateTimeField. В этом случае позволяет хранить только время как Python-объект datetime.time.
    link = models.URLField()  # Поле, реализующее CharField, но конкретно для хранения адресов интернет-страниц (URL).

    # https://docs.djangoproject.com/en/3.1/ref/models/fields/#module-django.db.models.fields


# one_to_one_relation = models.OneToOneField(some_model)
# one_to_many_relation = models.ForeignKey(some_model)
# many_to_many_relation = models.ManyToManyField(some_model)

# В данном коде some_model — это модель, к которой строится связь.
# Её можно передать как сам класс модели, так и название класса в виде строки.
# Снова обратимся к нашему примеру и восстановим связь «один ко многим» между сущностями Staff и Order.
# Заодно спроектируем последнюю.

