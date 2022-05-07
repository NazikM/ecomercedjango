import json

from django.http import JsonResponse
from django.shortcuts import render

from store.models import *


def store(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "store/Store.html", context=context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_total": 0, "get_cart_items": 0}
    context = {"items": items, "order": order}
    return render(request, "store/Cart.html", context=context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_total": 0, "get_cart_items": 0}
    context = {"items": items, "order": order}
    return render(request, "store/Checkout.html", context=context)


def updateItem(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    print(product_id, action)

    product = Product.objects.get(pk=product_id)
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created_item = OrderItem.objects.get_or_create(product=product, order=order)

    if action == "add":
        order_item.quantity += 1
    elif action == "remove":
        order_item.quantity -= 1

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()
    return JsonResponse("Item was added", safe=False)
