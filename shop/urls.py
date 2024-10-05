"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home`
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/',views.BASE,name='base'),
    path('',views.INDEX,name='index'),
    path('product/',views.PRODUCT,name='product'),
    path('search/',views.SEARCH,name='search'),
    path('products/<int:id>',views.PRODUCT_DETAIL_PAGE,name='product_details'),
    path('contact/',views.CONTACT,name='contact'),

    path('register/',views.HandelRegister,name='register'),

    path('login/',views.HandelLogin,name='login'),
    path('logout/',views.HandelLogout,name='logout'),

    path('checkout/',views.CHECKOUT,name='checkout'),

    path('placeorder/',views.PLACEORDER,name='placeorder'),

    path('meanswear/',views.MEANSWEAR,name = 'meanswear'),

    path('success/',views.SUCCESS,name='success'),


    #cart
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/',views.cart,name='cart'),



]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
