from django import template
from app.models.product import FavouriteProduct
from app.models.order import CartItem

register = template.Library()


@register.filter()
def is_liked(user, product) -> bool:
    if user.is_anonymous:
        return False
    return FavouriteProduct.objects.filter(user=user, product=product).exists()


@register.filter()
def is_added(user, product) -> bool:
    if user.is_anonymous:
        return False
    return CartItem.objects.filter(user=user, product=product).exists()


@register.filter()
def cart_item_quantity(user, product):
    try:
        if user.is_authenticated:
            return CartItem.objects.get(user=user, product=product).quantity
        return 0
    except CartItem.DoesNotExist:
        return 0


@register.filter()
def favourite_products_count(user):
    try:
        if user.is_authenticated:
            return FavouriteProduct.objects.all().filter(user=user).count()
        return 0
    except FavouriteProduct.DoesNotExist:
        return 0


@register.filter()
def cart_items_count(user):
    try:
        if user.is_authenticated:
            return CartItem.objects.all().filter(user=user).count()
        return 0
    except CartItem.DoesNotExist:
        return 0


@register.filter
def cart_total_sum(cart_list):
    return sum(cart.quantity * cart.product.current_price for cart in cart_list)


@register.filter
def cart_items_quantity(cart_list):
    return sum(cart.quantity for cart in cart_list)
