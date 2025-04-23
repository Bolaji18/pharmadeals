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
    path('accounts/profile/', views.index, name='index'),
    path('upload', views.pharma_upload, name='upload')

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)