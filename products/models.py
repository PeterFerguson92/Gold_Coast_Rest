from django.db import models
from enum import Enum


class CategoryChoice(Enum):
    LIVING_ROOM = "Living Room"
    BATHROOM = "Bathroom"
    BEDROOM = 'Bedroom'
    KITCHEN = "Kitchen"
    OUTDOOR = "Outdoor"


class Product(models.Model):
    title = models.CharField(max_length=64, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=25, choices=[(tag.name, tag.value) for tag in CategoryChoice], null=True)
    created_on = models.DateTimeField(auto_now_add=True),

    def __str__(self):
        """A string representation of the product model."""
        return self.title

