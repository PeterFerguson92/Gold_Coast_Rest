from django.db import models
from enum import Enum
from user.models import User

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


class Review(models.Model):
    BAD = 0
    LOW = 1
    NORMAL = 2
    GOOD = 3
    HIGH = 4
    EXCELLENT = 5
    RATING_CHOICES = ((BAD, 'Bad'), (LOW, 'Low'), (NORMAL, 'Normal'), (GOOD, 'Good'), (HIGH, 'High'),
                     (EXCELLENT, 'Excellent'))

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date inserted', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)

    def __str__(self):
        """A string representation of the review model."""
        return str(self.id) + ' - ' + self.product.title + ' - ' + str(self.pub_date)
