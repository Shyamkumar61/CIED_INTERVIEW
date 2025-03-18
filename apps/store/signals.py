from venv import create

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BillItem, Medicine


@receiver(post_save, sender=BillItem)
def reduce_quantity(sender, instance, created, **kwargs):
    print(instance.quantity)
    if created:
        try:
            med_instance = Medicine.objects.get(
                pk=instance.medicine.id, packaging_type=instance.packaging_type
            )
            med_instance.stock_quantity -= instance.quantity
            med_instance.save()
        except Medicine.DoesNotExist:
            print("Medicine does not exist")
    else:
        print("Bill already exists")
