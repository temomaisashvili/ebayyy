from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Product, Cart


def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'product_list.html', context)


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart, created = Cart.objects.get_or_create(customer=request.user)

    try:
        cart.add_to_cart(product)
        messages.success(request, "Product added to cart successfully!")
    except ValidationError as e:
        messages.error(request, f"Error: {e}")

    return redirect('product_list')


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(customer=request.user)
    context = {'cart': cart}
    return render(request, 'cart.html', context)
