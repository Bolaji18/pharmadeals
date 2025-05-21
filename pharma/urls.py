from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', auth_views.LoginView.as_view(template_name='pharma/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/profile/', views.profile, name='profile'),
    path('upload', views.pharma_upload, name='upload'),
    path('categories', views.category, name='category'),
    path('categories/<str:categor>/', views.product, name='product'),
    path('categories/<str:name>/<int:id>/', views.item, name='item'),
    path('get_pharma', views.get_pharma, name='get_pharma'),
    path('see_cart/', views.see_cart, name='see_cart'), 
    path('remove_from_cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('buynow/<str:name>/<int:id>/', views.buynow, name='buynow'),
    path('get_sales', views.get_sales, name='get_sales'),
    path('get_table', views.get_table, name='get_table'),
    path('pharma_delete/<int:id>/', views.pharma_delete, name='pharma_delete'),
    path('get_user', views.get_user, name='get_user'),
    path('purchase', views.purchase, name='purchase'),
    path('help', views.help, name='help'),
    path('bid/<int:id>/', views.bids_app, name='bid'),



    path('api/products/', views.product_list_api, name='product_list_api'),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)