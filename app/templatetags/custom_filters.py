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
        return CartItem.objects.get(user=user, product=product).quantity
    except CartItem.DoesNotExist:
        return 0


@register.filter()
def favourite_products_count(user):
    try:
        return FavouriteProduct.objects.all().filter(user=user).count()
    except FavouriteProduct.DoesNotExist:
        return 0


@register.filter()
def cart_items_count(user):
    try:
        return CartItem.objects.all().filter(user=user).count()
    except CartItem.DoesNotExist:
        return 0
