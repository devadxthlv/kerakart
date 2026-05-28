def cart_count(request):
    count = 0
    if 'cart' in request.session:
        cart = request.session['cart']
        for item in cart.values():
            count += item.get('qty', 0)
    return {'cart_count': count}
