from django.db.models.signals import post_save
from django.dispatch import receiver
 
from .models import Member, Ledger
 
 
@receiver(post_save, sender=Member)
def sync_member_ledger(sender, instance, created, **kwargs):
    ledger_name = instance.company_name or instance.owner_name
 
    if created:
        ledger = Ledger.objects.create(
            ledger_name=ledger_name,
            is_cash_or_bank=False,
        )
        instance.ledger = ledger
        instance.save(update_fields=["ledger"])
    else:
        # Keep the ledger name in sync if the member's name/company changes later
        if instance.ledger and instance.ledger.ledger_name != ledger_name:
            instance.ledger.ledger_name = ledger_name
            instance.ledger.save(update_fields=["ledger_name"])