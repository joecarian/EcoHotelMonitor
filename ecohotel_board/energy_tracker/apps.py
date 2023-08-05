"""
Configuration for the Energy Tracker Django application.

This module defines the configuration for the Energy Tracker Django application.
It provides settings related to the application.

Classes:
    - EnergyTrackerConfig: Represents the configuration for the Energy Tracker application.

"""

from django.apps import AppConfig


class EnergyTrackerConfig(AppConfig):
    """
    Configuration class for the Energy Tracker application.

    This class represents the configuration for the Energy Tracker application.
    It provides settings related to the application.

    Attributes:
        default_auto_field (str): The default auto-generated field for model primary keys.
        name (str): The name of the Energy Tracker application.

    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'energy_tracker'
