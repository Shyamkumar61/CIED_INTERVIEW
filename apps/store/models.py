from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Category(TimeStampedModel):

    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Supplier(TimeStampedModel):

    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Medicine(TimeStampedModel):

    PACKAGING_CHOICES = [
        ("single", "Single Piece"),
        ("strip", "Strip"),
        ("pack", "Pack"),
        ("box", "Box"),
    ]

    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="categories"
    )
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name="suppliers"
    )
    description = models.TextField(blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    packaging_type = models.CharField(max_length=10, choices=PACKAGING_CHOICES)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    expiry_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.packaging_type})"

    def get_single_price(self):
        price = self.price / self.stock_quantity
        return price


class Bill(TimeStampedModel):
    staff = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bills", to_field="email"
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Bill {self.id} - {self.staff.get_fullname()}"


class BillItem(TimeStampedModel):
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name="staff")
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    packaging_type = models.CharField(max_length=10, choices=Medicine.PACKAGING_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.medicine.name} - {self.quantity} {self.packaging_type}"
