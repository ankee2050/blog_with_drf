"""trydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from products.views import *
from blogs.views import LoginView, LogoutView
from rest_framework_swagger.views import get_swagger_view
from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )

schema_view = get_swagger_view(title="Blog API Documentation")

urlpatterns = [
    path('',home_view,name='home_view'),
    path('api_documentation/',schema_view),
    path('api/v1/', include('courses.api_urls')),
    path('blog_api/v1/', include('blogs.api_urls')),
    path('emp_api/v1/', include('registrations.api_urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('blog_api/v1/auth/', include('rest_framework.urls')),
    path('blog_api/v1/auth/login/', LoginView.as_view()),
    path('blog_api/v1/auth/logout/', LogoutView.as_view()),
    path('accounts/login/',include('registrations.urls')),
    path('blogs/',include('blogs.urls')),
    path('courses/',include('courses.urls')),
    path('contact/',contact_view,name='contact_view'),
    path('about/',about_view,name='about_view'),
    path('social/',social_view,name='social_view'),
    path('product/<int:my_id>/',product_detail_view,name='product-details'),
    path('create/',product_create_view,name='product_create'),
    path('admin/', admin.site.urls),
]
