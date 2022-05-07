import datetime

from django.http import JsonResponse
from django.shortcuts import render

from store.models import *
from .utils import *


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        data = cookieCart(request)
        order = data["order"]
    products = Product.objects.all()
    context = {"products": products, "order": order}
    return render(request, "store/Store.html", context=context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        data = cookieCart(request)
        items = data["items"]
        order = data["order"]
    context = {"items": items, "order": order}
    return render(request, "store/Cart.html", context=context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        data = cookieCart(request)
        items = data["items"]
        order = data["order"]
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


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(customer=customer,
                                           order=order,
                                           address=data['shipping']['address'],
                                           city=data['shipping']['city'],
                                           state=data['shipping']['state'],
                                           zipcode=data['shipping']['zipcode'],)
    else:
        print("User is not logged in")
    return JsonResponse("Payment complete!", safe=False)
