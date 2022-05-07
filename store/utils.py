import json

from store.models import Product


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