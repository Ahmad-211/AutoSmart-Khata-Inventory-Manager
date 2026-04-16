from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SaleItem

@receiver(post_save, sender=SaleItem)
def process_sale_transaction(sender, instance, created, **kwargs):
    """
    Automates inventory and ledger management whenever a SaleItem is created.
    """
    if created:
        # 1. UNIVERSAL STOCK DEDUCTION
        # This happens for both CASH and CREDIT sales.
        part = instance.part
        part.stock_qty -= instance.quantity
        part.save()

        # 2. CONDITIONAL KHATA (LEDGER) UPDATE
        # We only increase the customer's debt if the sale is on Credit.
        sale = instance.sale
        if sale.payment_type == 'CREDIT' and sale.customer:
            customer = sale.customer
            
            # Calculate total for this specific item (Price * Quantity)
            item_total = instance.quantity * instance.price_at_sale
            
            # Update the running balance
            customer.current_balance += item_total
            customer.save()
            
            # Optional: Log to console for debugging
            print(f"✅ KHATA UPDATED: {customer.name} balance increased by {item_total}")
        
        elif sale.payment_type == 'CASH':
            print(f"✅ CASH SALE: Stock reduced for {instance.part.name}, no change to Khata.")