from django.db import models


# Create your models here.
class Collection(models.Model):
    title = models.CharField(max_length=255)


class Promotion(models.Model):
    promo_description = models.CharField(max_length=255)
    discount = models.FloatField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)

    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
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


class Order(models.Model):
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
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True
    )


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField
