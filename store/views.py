import datetime
import json

from django.http import JsonResponse
from django.shortcuts import render

from store.models import *


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        order = {"get_cart_items": 0}
    products = Product.objects.all()
    context = {"products": products, "order": order}
    return render(request, "store/Store.html", context=context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except KeyError:
            cart = {}
        items = []
        order = {"get_total": 0, "get_cart_items": 0, "shipping": False}
        for i in cart:
            order["get_cart_items"] += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = product.price * order["get_cart_items"]
            order["get_total"] += total
            items.append({
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "imageURL": product.imageURL
                },
                "quantity": cart[i]['quantity'],
                "get_total": total
            })

            if not product.digital:
                order["shipping"] = True
    context = {"items": items, "order": order}
    return render(request, "store/Cart.html", context=context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_total": 0, "get_cart_items": 0, "shipping": False}
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
