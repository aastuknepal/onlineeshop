from django.shortcuts import render
from shop.models import Category, Customer, Product, Cart
from shop.recommendations import calculate_item_similarity  # Import recommendation function
from shop.models import Customer, Product, Review, Cart, Wishlist


def productdetail(request, prid):
    current_user = request.user
    product = Product.objects.get(id=prid)

    # Recommendation logic - calculate similar products
    recommended_products = calculate_item_similarity(product)

    customer = []
    try:
        customer = Customer.objects.get(user_id=current_user.id)
    except:
        pass

    reviews = Review.objects.filter(product_id=prid)
    carts = Cart.objects.filter(user_id=current_user.id)
    wishlist = Wishlist.objects.filter(user_id=current_user.id, product_id=prid)

    try:
        pr_qty = Cart.objects.get(user_id=current_user.id, product_id=prid)
        pr_qty = pr_qty.qty
    except:
        pr_qty = 0

    no_of_reviews = len(reviews)
    
    rating = 0
    for review in reviews:
        rating = rating + review.rating
    try:
        rating = rating / no_of_reviews
    except:
        pass

    desc = product.description
    descs = list(desc.split("#"))

    qty = 0
    total = 0
    for cart in carts:
        total = total + cart.amount
        qty = qty + cart.qty
    
    details = {
        'customer': customer,
        'product': product,
        'descs': descs,
        'reviews': reviews,
        'no_of_reviews': no_of_reviews,
        'rating': rating,
        'qty': qty,
        'total': total,
        'carts': carts,
        'wishlist': wishlist,
        'pr_qty': pr_qty,
        'recommended_products': recommended_products  # Add recommended products to the context
    }
    
    return render(request, 'productdetail.html', details)
