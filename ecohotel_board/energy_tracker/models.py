"""
Models for the EcoHotel energy report application.

This module defines the models used in the EcoHotel energy report application.
The models represent the entities in the application, such as EcoHotels and Reports.

Models:
    - EcoHotel: Represents an EcoHotel entity with a name field.
    - Report: Represents an energy report entity with fields for an associated EcoHotel,
              energy produced, energy consumed, date, hash, and transaction ID.
"""

import hashlib
from django import forms
from django.db import models
from blockchain.blockchain_writer import BlockchainWriter
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.conf import settings


class EcoHotel(models.Model):
    """
    Model representing an EcoHotel entity.

    Attributes:
        name (TextField): The name of the EcoHotel.

    """

    name = models.TextField(default='Pomelia', max_length=20, null=True)


class Report(models.Model):
    """
    Model representing an energy report entity.

    Attributes:
        ecohotel (ForeignKey): The associated EcoHotel for the energy report.
        energy_produced (BigIntegerField): The amount of energy produced.
        energy_consumed (BigIntegerField): The amount of energy consumed.
        date (DateField): The date of the report.
        hash (CharField): The hash of the report.
        txId (CharField): The transaction ID of the report.
        _note (str): A string representation of the report note.

    Methods:
        write_on_chain(): Writes the report on the blockchain.

    """

    ecohotel = models.ForeignKey(EcoHotel, on_delete=models.CASCADE)
    energy_produced = models.BigIntegerField(default=0)
    energy_consumed = models.BigIntegerField(default=0)
    date = models.DateField(auto_now=True)
    hash = models.CharField(max_length=32, default=None, null=True)
    txId = models.CharField(max_length=66, default=None, null=True)
    _note = f"Energy Produced: {energy_produced}\t Energy Consumed: {energy_consumed}"

    def write_on_chain(self):
        """
        Write the report on the blockchain.

        This method calculates the hash of the report and sends it as a transaction to the blockchain network.

        """

        self.hash = hashlib.sha256(self._note.encode('utf-8')).hexdigest()
        self.txId = BlockchainWriter().send_transaction(self.hash)
        self.save()
