"""
Module: forms

This module contains form classes related to user authentication and registration.

Classes:
- FormSignIn: Form for user sign-in.

"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class FormSignIn(UserCreationForm):
    """
    FormSignIn class.

    This form is used for user sign-in and extends the built-in UserCreationForm provided by Django.

    Attributes:
        email (forms.CharField): Field for user email.

    Meta:
        model (User): The user model used for the form.
        fields (list): The list of fields to be included in the form.

    """

    email = forms.CharField(max_length=30, required=True, widget=forms.EmailInput())

    class Meta:
        """
        Meta class.

        Specifies the user model and the fields used in the form.

        Attributes:
            model (User): The user model used for the form.
            fields (list): The list of fields to be included in the form.

        """

        model = User
        fields = ["username", "email", "password1", "password2"]
