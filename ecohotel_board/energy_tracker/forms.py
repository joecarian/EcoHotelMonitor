"""
Module: ecohotels.forms

This module contains form classes related to eco-friendly hotels and energy reports.

Classes:
- ReportForm: Form for collecting data on energy production and consumption in an eco-friendly hotel.

Global Variables:
- ECOHOTELS_CHOICES: Choices for the eco-friendly hotel names in the report form.

"""

from django import forms
from .models import EcoHotel

ECOHOTELS_CHOICES = [(index, data) for index, data in enumerate(
    EcoHotel.objects.values_list('name', flat=True))]


class ReportForm(forms.Form):
    """
    Report Form class.

    This class defines a report form for collecting data related to energy production
    and consumption in an eco-friendly hotel.

    Attributes:
        name (ChoiceField): Field for selecting the name of the eco-friendly hotel.
        energy_produced (IntegerField): Field for entering the energy produced by the hotel.
        energy_consumed (IntegerField): Field for entering the energy consumed by the hotel.

    """
    name = forms.ChoiceField(choices=ECOHOTELS_CHOICES)
    energy_produced = forms.IntegerField()
    energy_consumed = forms.IntegerField()
