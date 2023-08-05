"""This module contains view-based classes for handling HTTP requests.

List of classes:
- SignInView: View for the "Sign Up" page.
- CustomLoginView: View for the "Login" page.
- CustomLogoutView: View for the "Logout" page.
"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from .utils import AccessLog
from accounts.forms import FormSignIn
from django.contrib import messages
from django.contrib.auth.views import LogoutView


class SignUpView(FormView):
    """
    SignOutView class.

    This class is a view for signing out users.

    Attributes:
        template_name (str): The name of the template to be rendered.
        form_class (Form): The form class used for the view.
        success_url (str): The URL to redirect to after successful form submission.

    Methods:
        form_valid(form): Performs actions when the form is valid.

    """

    template_name = "accounts/sign_up.html"
    form_class = FormSignIn
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """
        Handle form validation.

        This method is executed when the submitted form is valid.
        It creates a new user with the provided username, email, and password.
        Then, it authenticates and logs in the user.

        Args:
            form (Form): The validated form instance.

        Returns:
            HttpResponse: The response after processing the form.

        """
        response = super().form_valid(form)
        username = form.cleaned_data["username"]
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password1"]
        User.objects.create_user(
            username=username, password=password, email=email)
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response


class CustomLoginView(LoginView):
    """
    CustomLoginView class.

    This class extends the built-in LoginView class provided by Django to customize the login process.

    Attributes:
        template_name (str): The name of the template to be rendered.
        success_url (str): The URL to redirect to after successful login.

    Methods:
        form_valid(form): Performs actions when the form is valid.
        get(request, *args, **kwargs): Handles GET requests.

    """

    template_name = 'accounts/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """
        Handle form validation.

        This method is executed when the submitted form is valid.
        It performs additional actions after successful login, such as logging the IP address
        and displaying a warning message if necessary.

        Args:
            form (Form): The validated form instance.

        Returns:
            HttpResponse: The response after processing the form.

        """
        response = super().form_valid(form)
        user = form.get_user()
        ip_address = self.request.META.get('REMOTE_ADDR')
        message = AccessLog().log_last_ip(user, ip_address)
        if message:
            messages.warning(self.request, message)
        return response

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.

        This method handles GET requests to the login view.
        If the user is already authenticated, it redirects to the success URL.
        Otherwise, it calls the parent class method to render the login form.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The response for the GET request.

        """
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)


class CustomLogoutView(LogoutView):
    """
    CustomLogoutView class.

    This class extends the built-in LogoutView class provided by Django to customize the logout process.

    Attributes:
        next_page (str): The URL to redirect to after successful logout.

    Methods:
        dispatch(request, *args, **kwargs): Handles the view's dispatch process.

    """

    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        """
        Handle the view's dispatch process.

        This method handles the view's dispatch process by performing additional actions during logout,
        such as deleting the user session and logging out the user.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The response after processing the dispatch.

        """
        logout(request)
        request.session.delete()
        return super().dispatch(request, *args, **kwargs)
