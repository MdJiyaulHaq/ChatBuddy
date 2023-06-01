from django.db import models


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField()
    birth_date = models.DateField(null=True)

    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_SILVER = "S"
    MEMBERSHIP_GOLD = "G"

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, "BRONZE"),
        (MEMBERSHIP_SILVER, "SILVER"),
        (MEMBERSHIP_GOLD, "GOLD"),
    ]

    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE
    )


class Order:
    placed_at = models.DateField(auto_now_add=True)
    PAYMENT_STAUS_PENDING = "P"
    PAYMENT_STAUS_COMPLETE = "C"
    PAYMENT_STAUS_FAILED = "F"
    PAYMENT_STAUS_CHOICES = [
        (PAYMENT_STAUS_PENDING, "PENDING"),
        (PAYMENT_STAUS_COMPLETE, "COMPLETE"),
        (PAYMENT_STAUS_FAILED, "FAILED"),
    ]
    payment_status = models.CharField(
        max_length=255, choices=PAYMENT_STAUS_CHOICES, default=PAYMENT_STAUS_PENDING
    )


class Address:
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True
    )
