"""
Configuration for the Accounts Django application.

This module defines the configuration for the Accounts Django application.
It includes the AppConfig subclass for the application.

Classes:
    - AccountsConfig: Represents the configuration for the Accounts application.

"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Configuration class for the Accounts application.

    This class represents the configuration for the Accounts application.
    It provides the necessary configurations for the application to function.

    Attributes:
        name (str): The name of the application.

    """
    name = 'accounts'
