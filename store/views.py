from django.shortcuts import render

from store.models import Product


def store(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "store/Store.html", context=context)


def cart(request):
    context = {}
    return render(request, "store/Cart.html", context=context)


def checkout(request):
    context = {}
    return render(request, "store/Checkout.html", context=context)
