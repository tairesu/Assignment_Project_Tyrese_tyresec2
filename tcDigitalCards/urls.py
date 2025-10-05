"""
URL configuration for tcDigitalCards project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from cardManager import views
from cardManager.views import UserRegistration
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('card/<str:card_token>/', views.card_detail, name='card_view'),
    path('card/<str:card_token>/activate/', views.CardDetail.as_view(), name='card_activate_view'),
    path('card/<int:pk>/update/', views.CardUpdate.as_view(), name='card_update_view'),
    path('profile/create/', views.ProfileCreate.as_view(), name='profile_create_view'),
    path('profile/<str:profile_slug>/', views.ProfileDetail.as_view(), name='profile_view'),
    path('profile/<int:pk>/update/', views.ProfileUpdate.as_view(), name='profile_update_view'),
    path('dashboard/', views.UserDashboard.as_view(), name='dashboard_view'),
    path('register/', views.UserRegistration.as_view(), name='register_view'),
    path('login/', views.LoginView.as_view(), name='login_view'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout_view'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
