# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone
from .models import Item, Notification

@receiver(post_save, sender=Item)
def generate_expiry_notifications(sender, instance, created, **kwargs):
    if created:
        thrushold = timezone.now().date()  + timedelta(days=2)
        get_products = Item.objects.filter(expiring_date=thrushold)
        if get_products:
            message = "The product  is expiring soon."
            Notification.objects.create( message=message)
