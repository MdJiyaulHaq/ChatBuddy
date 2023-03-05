from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateField(auto_now=True)


class Customer (models.Model):
    membership_bronze = 'B'
    membership_silver = 'S'
    membership_gold = 'G'
    membership_choices = [
        (membership_bronze, 'Bronze'),
        (membership_silver, 'Silver')
        (membership_gold, 'Gold')
    ]
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)


membership = models.CharField(
    max_length=1, choices=membership_choices, default=membership_bronze)


class Order(models.Model):
    placed_at = models.DateTimeField(auto_now_add=True)

    status_pending = 'P'
    status_complete = 'C'
    status_failed = 'F'

    pament_choices = [
        (status_pending, 'Pending'),
        (status_complete, 'Complete'),
        (status_failed, 'Failed')
    ]
    payment_status = models.CharField(
        max_length=1, choices=payment_choices, default=status_pending)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True)
    

class Phone(models.Model):
    phone = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
