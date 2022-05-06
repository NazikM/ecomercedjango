from django.shortcuts import render


def store(request):
    context = {}
    return render(request, "store/Store.html", context=context)


def cart(request):
    context = {}
    return render(request, "store/Cart.html", context=context)


def checkout(request):
    context = {}
    return render(request, "store/Checkout.html", context=context)
