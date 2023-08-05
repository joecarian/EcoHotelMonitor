"""
Module: urls

This module contains the URL patterns for the accounts app.

URL Patterns:
- /registrazione/ -> SignOutView: URL pattern for user registration.
- /login/ -> CustomLoginView: URL pattern for user login.
- /logout/ -> CustomLogoutView: URL pattern for user logout.

"""

from django.urls import path
from .views import SignUpView, CustomLoginView, CustomLogoutView

urlpatterns = [
    path('sign_up/', SignUpView.as_view(), name='sign_up_view'),
    path('login/', CustomLoginView.as_view()),
    path('logout/', CustomLogoutView.as_view(), name='logout_view')
]
