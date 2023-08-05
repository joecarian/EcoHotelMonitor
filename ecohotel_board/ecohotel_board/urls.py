"""ecohotel_board URL Configuration

This module configures the URL patterns for the ecohotel_board application.
The `urlpatterns` list routes URLs to views, including paths for the admin interface,
Jet admin dashboard, energy_tracker app, and authentication-related URLs.

"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('energy_tracker.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
