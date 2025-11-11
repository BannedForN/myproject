from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from knifestore.models import Knife, Order, OrderItem, Customer
from .basket import Basket
from django.utils import timezone
from .forms import *

@login_required
def basket_update(request):
    basket = request.session.get('basket', {})

    for product_id in basket.keys():
        key = f'count_{product_id}'
        if key in request.POST:
            try:
                new_count = int(request.POST[key])
                if new_count > 0:
                    basket[product_id]['count'] = new_count
                else:
                    del basket[product_id]
            except ValueError:
                continue  # Игнорируем ошибочные значения

    request.session['basket'] = basket
    return redirect('basket_detail')

@login_required
def basket_detail(request):
    basket = Basket(request)
    return render(request, 'basket/detail.html', context={'basket': basket})

@login_required
def basket_remove(request, product_id):
    basket = Basket(request)
    product = get_object_or_404(Knife, pk=product_id)
    basket.remove(product)
    return redirect('basket_detail')

@login_required
def basket_clear(request):
    basket = Basket(request)
    basket.clear()
    return redirect('basket_detail')

@login_required
@require_POST
def basket_add(request, product_id):
    basket = Basket(request)
    product = get_object_or_404(Knife, pk=product_id)
    form = BasketAddProductForm(request.POST)
    if form.is_valid():
        basket.add(
            product=product,
            count=form.cleaned_data['count'],
            update_count=form.cleaned_data['reload']
        )
    return redirect('basket_detail')

@login_required
def basket_buy(request):
    basket = Basket(request)
    if basket.__len__() <= 0:
        return redirect('list_product_filter')
    form = OrderForm(request.POST)
    if form.is_valid():
        order = Order.objects.create(
            customer = form.cleaned_data['customer'],
            order_date = form.cleaned_data['order_date'],
            status = form.cleaned_data['status'],
            total_amount = form.cleaned_data['total_amount'],
            shipping_address = form.cleaned_data['shipping_address']
        )
        order.price = basket.get_total_price()
        for item in basket:
            orderitem = OrderItem.objects.create(
                knife = item['product'],
                count = item['count'],
                order = order
            )
        basket.clear()
    return redirect('basket_detail')

@login_required
def open_order(request):
    basket = Basket(request)

    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        return redirect('customer_create')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = customer
            order.order_date = timezone.now()
            order.total_amount = 0
            order.save()

            total = 0
            for item in basket:
                OrderItem.objects.create(
                    order=order,
                    knife=item['product'],
                    quantity=item['count'],
                    price=item['product'].price
                )
                total += item['count'] * item['product'].price

            order.total_amount = total
            order.save(update_fields=['total_amount'])

            basket.clear()

    else:
        form = OrderForm(initial={
            'customer': customer.id,
            'status': 'new',
            'shipping_address': customer.address,
        })

    return render(request, 'order/order_form.html', {'form_order': form})