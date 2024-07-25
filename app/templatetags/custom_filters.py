from django import template
from app.models.product import FavouriteProduct

register = template.Library()


@register.filter()
def is_liked(user, product) -> bool:
    if user.is_anonymous:
        return False
    return FavouriteProduct.objects.filter(user=user, product=product).exists()
