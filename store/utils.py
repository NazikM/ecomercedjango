import json

from store.models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except KeyError:
        cart = {}
    items = []
    order = {"get_total": 0, "get_cart_items": 0, "shipping": False}
    for i in cart:
        order["get_cart_items"] += cart[i]['quantity']
        product = Product.objects.get(id=i)
        total = product.price * cart[i]['quantity']
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
    return {"items": items, 'order': order}


def guestOrder(request, data):
    print("User is not logged in")
    name = data["form"]["name"]
    email = data["form"]["email"]

    cookieData = cookieCart(request)
    items = cookieData["items"]
    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )
    for item in items:
        product = Product.objects.get(id=item["product"]["id"])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item["quantity"]
        )
    return order, customer
