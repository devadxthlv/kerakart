from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def home(request):
    categories = Category.objects.all()
    # Fetch first 8 available products as featured
    featured_products = Product.objects.filter(is_available=True)[:8]
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'store/home.html', context)

def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)
    
    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)
        
    context = {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
    }
    return render(request, 'store/products.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    context = {
        'product': product,
    }
    return render(request, 'store/product_detail.html', context)

