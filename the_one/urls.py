"""
URL configuration for the_one project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Frontend pages
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # Chatbot
    path('chatbot/', views.chatbot_view, name='chatbot'),
    
    # Booking
    path('booking/', views.booking_create_view, name='booking_create'),
    path('bookings/', views.booking_list_view, name='booking_list'),
    path('motorcycles/', views.motorcycle_list_view, name='motorcycle_list'),
    
    # Mechanic
    path('mechanic/dashboard/', views.mechanic_dashboard_view, name='mechanic_dashboard'),
    
    # API endpoints
    path('api/users/', include('users.urls')),
    path('api/chatbot/', include('chatbot.urls')),
    path('api/booking/', include('booking.urls')),
    path('api/mechanics/', include('mechanics.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
