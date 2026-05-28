from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from store.models import Product
import decimal

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    grand_total = decimal.Decimal('0.00')
    
    for product_id, item_data in cart.items():
        price = decimal.Decimal(item_data['price'])
        qty = int(item_data['qty'])
        item_total = price * qty
        grand_total += item_total
        
        cart_items.append({
            'product_id': product_id,
            'name': item_data['name'],
            'price': price,
            'qty': qty,
            'unit': item_data['unit'],
            'image_url': item_data.get('image_url'),
            'slug': item_data.get('slug'),
            'total': item_total
        })
        
    context = {
        'cart_items': cart_items,
        'grand_total': grand_total,
    }
    return render(request, 'cart/cart.html', context)

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        qty = int(request.POST.get('quantity', 1))
        
        # Check stock limits
        if qty > product.stock:
            messages.error(request, f"Sorry, only {product.stock} units of {product.name} are available in stock.")
            return redirect(request.META.get('HTTP_REFERER', 'store:product_list'))
            
        cart = request.session.get('cart', {})
        str_id = str(product_id)
        
        if str_id in cart:
            new_qty = cart[str_id]['qty'] + qty
            if new_qty > product.stock:
                messages.error(request, f"Cannot add more. Only {product.stock} units are in stock.")
                return redirect(request.META.get('HTTP_REFERER', 'store:product_list'))
            cart[str_id]['qty'] = new_qty
        else:
            cart[str_id] = {
                'name': product.name,
                'price': str(product.price),
                'qty': qty,
                'unit': product.unit,
                'image_url': product.image.url if product.image else None,
                'slug': product.slug
            }
            
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f"Successfully added {product.name} to your cart.")
        
    return redirect('cart:cart_detail')

def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        str_id = str(product_id)
        
        if str_id in cart:
            item_name = cart[str_id]['name']
            del cart[str_id]
            request.session['cart'] = cart
            request.session.modified = True
            messages.success(request, f"Removed {item_name} from your cart.")
            
    return redirect('cart:cart_detail')


