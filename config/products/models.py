from django.db import models
from django.conf import settings
from django.db.models import CheckConstraint, Q


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name




class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(price__gt=0),
                name='price_positive'
            ),
            CheckConstraint(
                check=Q(stock__gte=0),
                name='stock_non_negative'
            )
        ]

    def __str__(self):
        return self.name