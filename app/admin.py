from django.contrib import admin
from app.models import Category, Product, ProductImage
from mptt.admin import MPTTModelAdmin
from .forms import CategoryAdminForm, ProductAdminForm


class ProductImageStackedInline(admin.StackedInline):
    model = ProductImage
    extra = 3
    min_num = 0


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('id', 'name', )
    list_display_links = ('id', 'name', )
    list_filter = ('name', )
    form = CategoryAdminForm


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('id', 'name', 'price', 'category', 'quantity', )
    list_display_links = ('id', 'name', 'price', )
    list_filter = ('name', 'price', 'category', )
    inlines = (ProductImageStackedInline,)


