from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView, DetailView, View, CreateView
from .models import Product, Category, CartItem, FavouriteProduct
from .forms import UserRegisterModelForm

from django.views.generic import ListView
from .models import Product, Category, CartItem


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "app/product/product-list.html"
    model = Product
    paginate_by = 2
    context_object_name = 'products'

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.request.GET.get('category')
        if category_id:
            qs = qs.filter(category__id=category_id)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['categories'] = Category.objects.all()

        return context


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'app/product/product-details.html'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['categories'] = Category.objects.all()

        return context


class RegisterCreateView(CreateView):
    template_name = 'app/auth/register.html'
    form_class = UserRegisterModelForm
    success_url = reverse_lazy('login_page')

    def form_valid(self, form):
        form.save()
        # username = form.cleaned_data.get('username')
        # password = form.cleaned_data.get('password')
        # user = authenticate(self.request, username=username, password=password)
        # if user is not None:
        #     login(self.request, user)
        # else:
        #     print("Authentication failed for user:", username)

        # send_to_email('Your account has been created!', form.data['email'])
        # send_to_email.delay('Your account has been created!', form.data['email'])
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class LogoutView(TemplateView):
    template_name = 'app/auth/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product_id=pk)

        if not created:
            cart_item.delete()

        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('product_detail', pk=pk)


class DeleteFromCartView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        cart_item = CartItem.objects.get(id=pk)
        cart_item.delete()

        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('product_detail', pk=pk)


class IncreaseCartView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product_id=pk)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('product_detail', pk=pk)


class DecreaseCartView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product_id=pk)

        if not created and cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('product_detail', pk=pk)


class FavouriteProductView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        product, created = FavouriteProduct.objects.get_or_create(user=request.user, product_id=pk)

        if not created:
            product.delete()

        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('product_detail', pk=pk)


class CartDetailsView(LoginRequiredMixin, ListView):
    queryset = CartItem.objects.all()
    template_name = 'app/order/cart-list.html'
    context_object_name = 'cart_list'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['categories'] = Category.objects.all()

        return context

