from django.db.models import Model, ForeignKey, CASCADE, PositiveIntegerField, BooleanField


class CartItem(Model):
    user = ForeignKey('app.User', related_name='user_cart_items', on_delete=CASCADE)
    product = ForeignKey('app.Product', related_name='product_cart_items', on_delete=CASCADE)
    quantity = PositiveIntegerField(default=1)
    is_added = BooleanField(blank=True, null=True)

    def __str__(self):
        return self.product.name

    @property
    def amount(self):
        return self.quantity * self.product.current_price

