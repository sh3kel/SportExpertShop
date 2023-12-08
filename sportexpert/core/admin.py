from django.contrib import admin
from .models import *

class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'price',
        'discount_price',
        'cat',
        'sex',
        'mainphoto',
    ]

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'start_date',
        'ordered_date',
        'ordered',
        'coupon'
    ]

class CouponAdmin(admin.ModelAdmin):
    list_display = [
        'code',
        'amount',
    ]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "ordered",
        "item",
        "quantity",
    ]

class PostAddressAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "first_name",
        "last_name",
        "email",
        "address",
        "post_index",
    ]

admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(PostAddress, PostAddressAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Category)

admin.site.site_title = 'SportExpert'
