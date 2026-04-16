from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    current_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=50000.00)

    def __str__(self):
        return f"{self.name} ({self.phone})"

class Part(models.Model):
    name = models.CharField(max_length=255)
    oem_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    brand = models.CharField(max_length=100) # e.g., Hino, Toyota, Isuzu
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_qty = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.brand} - {self.name}"

class Sale(models.Model):
    PAYMENT_CHOICES = [('CASH', 'Cash'), ('CREDIT', 'Credit')]
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale {self.id} - {self.payment_type}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.part.name}"