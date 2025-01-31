from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from .views import (ProductListView, RegisterCreateView, LogoutView, ProductDetailView, AddToCartView,
                    FavouriteProductView, IncreaseCartView, DecreaseCartView, CartDetailsView, DeleteFromCartView)


urlpatterns = [
    path('', ProductListView.as_view(), name='product_list_page'),
    path('product/detail/<uuid:pk>/', ProductDetailView.as_view(), name='product_detail_page'),
    #path('settings', SettingsUpdateView.as_view(), name='settings_page'),
    path('register', RegisterCreateView.as_view(), name='register_page'),
    path('login', LoginView.as_view(
        template_name='app/auth/login.html',
        redirect_authenticated_user=True,
        next_page='product_list_page',
    ), name='login_page'),
    path('logout', LogoutView.as_view(), name='logout_page'),

    path('cart/add/<uuid:pk>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/increase/<uuid:pk>/', IncreaseCartView.as_view(), name='increase_cart'),
    path('cart/decrease/<uuid:pk>/', DecreaseCartView.as_view(), name='decrease_cart'),
    path('cart/delete/<uuid:pk>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('favourite-product/add/<uuid:pk>/', FavouriteProductView.as_view(), name='add_favourite_product'),
    path('cart/details/', CartDetailsView.as_view(), name='cart_details_page'),
]
