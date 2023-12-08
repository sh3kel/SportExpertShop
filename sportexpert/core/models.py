from django.conf import settings
from django.db import models
from django.urls import reverse


SEX_CHOICES = (
    ('M', 'Мужское'),
    ('W', 'Женское'),
    ('MK', 'Мальчик'),
    ('WK', 'Девочка'),
    ('U', 'Унисекс'),
)

LABEL_CHOICES = (
    ('P', 'Новое'),
    ('S', 'Распродажа'),
    ('D', 'Хит'),
)

class Item(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    price = models.FloatField(verbose_name='Цена')
    discount_price = models.FloatField(blank=True, null=True, verbose_name='Цена по скидке')
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Категория')
    sex = models.CharField(choices=SEX_CHOICES, max_length=2, verbose_name='Пол')
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, verbose_name='Лейбл')
    slug = models.SlugField(verbose_name='URL')
    description = models.TextField(verbose_name='Описание')
    mainphoto = models.ImageField(blank=True, null=True, verbose_name='Заглавное фото')
    photo1 = models.ImageField(blank=True, null=True, verbose_name='Фото №1')
    photo2 = models.ImageField(blank=True, null=True, verbose_name='Фото №2')
    photo3 = models.ImageField(blank=True, null=True, verbose_name='Фото №3')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:products", kwargs= { 'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории товаров"

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='Пользователь')
    ordered = models.BooleanField(default=False, verbose_name='Оплачен')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_discount(self):
        return self.get_total_item_price() - self.get_total_discount_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_price()
        return self.get_total_item_price()

    class Meta:
        verbose_name = "Товар в работе"
        verbose_name_plural = "Товары в работе"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='Пользователь')
    items = models.ManyToManyField(OrderItem, verbose_name='Товары')
    start_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    ordered_date = models.DateTimeField(verbose_name='Дата оплаты')
    ordered = models.BooleanField(default=False, verbose_name='Оплачен')
    post_address = models.ForeignKey('PostAddress', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Адрес доставки')
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Промокод')

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total = total + order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"



class PostAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='E-mail')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    post_index = models.CharField(max_length=100, verbose_name='Почтовый индекс')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Адрес заказа"
        verbose_name_plural = "Адреса заказов"

class Coupon(models.Model):
    code = models.CharField(max_length=15, verbose_name='Промокод')
    amount = models.FloatField(blank=True, null=True, verbose_name='Сумма скидки')
    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"
