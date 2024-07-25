import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from mptt.models import MPTTModel
from django_ckeditor_5.fields import CKEditor5Field
from datetime import timedelta
from django.utils.timezone import now


class Category(MPTTModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'

    class MPTTMeta:
        order_insertion_by = ['name']

    @property
    def has_children(self):
        return self.children.exists()


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    category = models.ForeignKey('app.Category', on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.PositiveSmallIntegerField(default=0)
    quantity = models.PositiveSmallIntegerField(default=0)
    short_description = CKEditor5Field('Text', config_name='extends')
    description = CKEditor5Field('Text', config_name='extends')
    tags = models.TextField()
    specifications = models.JSONField(default=dict)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(discount_percent__lte=100),
                name='discount_percent_checker'
            )
        ]

    @property
    def is_new(self) -> bool:
        return self.created_at >= now() - timedelta(days=7)

    @property
    def is_stock(self):
        return self.quantity > 0

    @property
    def current_price(self):
        return self.price - (self.price * self.discount_percent // 100)

    @property
    def get_specifications(self):
        return list(self.specifications.values())[:5]

    @property
    def get_all_specifications(self):
        return list(self.specifications.items())


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    product = models.ForeignKey('app.Product', models.CASCADE, related_name='images')


class User(AbstractUser):
    pass
