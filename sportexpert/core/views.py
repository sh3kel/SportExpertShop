from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import *
from django.views.generic import ListView, DetailView, View

from .models import *

def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "core/products.html", context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'form': form,
            'couponform': CouponForm(),
            'object': order,
        }
        return render(self.request, "core/checkout.html", context)
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                address = form.cleaned_data.get('address')
                post_index = form.cleaned_data.get('post_index')
                post_address = PostAddress(
                    user=self.request.user,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    address=address,
                    post_index=post_index,
                )

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.ordered = True
                post_address.save()
                order.post_address = post_address
                order.save()
                messages.success(self.request, 'Заказ оформлен!')
                return redirect('core:home')

            messages.warning(self.request, 'Ошибка оформления заказа.')
            return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, 'У вас нет активных заказов')
            return redirect('core:cart')

        messages.warning(self.request, 'Ошибка оформления заказа.')
        return redirect('core:checkout')

class HomeView(ListView):
    model = Item
    paginate_by = 6
    template_name = "core/home.html"


class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'core/cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'У вас нет активных заказов')
            return render(self.request, 'core/cart.html')

class ItemDetailView(DetailView):
    model = Item
    template_name = "core/products.html"
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Количество товара в корзине обновлено!")
        else:
            messages.info(request, "Товар добавлен в корзину!")
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Товар добавлен в корзину!")
    return redirect("core:products", slug=slug)
@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, "Товар удален из корзины!")
            return redirect("core:products", slug=slug)
        else:
            messages.info(request, "Данного товара нет в корзине!")
            return redirect("core:products", slug=slug)
    else:
        messages.info(request, "Вы еще ничего не заказали!")
        return redirect("core:products", slug=slug)

@login_required()
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, "Количество обновлено!")
            else:
                order.items.remove(order_item)
                messages.info(request, "Товар удален из корзины")
            return redirect("core:cart")


@login_required()
def trash_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, "Товар удален из корзины!")
            return redirect("core:cart")


@login_required()
def add_single_item_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Количество обновлено!")
            return redirect("core:cart")

def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, 'Такого купона не существует')
        return redirect('core:checkout')



class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, 'Купон успешно применен')
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, 'У вас нет активных заказов')
                return redirect("core:checkout")