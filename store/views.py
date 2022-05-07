from django.shortcuts import render

from store.models import Product, Order


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
