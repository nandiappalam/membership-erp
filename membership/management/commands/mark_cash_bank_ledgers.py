from django.core.management.base import BaseCommand
from membership.models import Ledger
 
 
class Command(BaseCommand):
    help = "Flags existing Cash/Bank ledgers based on their group name so voucher auto-filtering works."
 
    def handle(self, *args, **options):
        # Adjust these keywords to match your actual Group names in Tally/your Ledger table
        cash_bank_keywords = ["cash", "bank"]
 
        updated = 0
        for keyword in cash_bank_keywords:
            count = Ledger.objects.filter(
                group__name__icontains=keyword,
                is_cash_or_bank=False,
            ).update(is_cash_or_bank=True)
            updated += count
            self.stdout.write(f"Marked {count} ledger(s) matching group '*{keyword}*'")
 
        self.stdout.write(self.style.SUCCESS(f"Done. {updated} ledger(s) updated in total."))
 
        # Quick sanity check
        remaining = Ledger.objects.filter(is_cash_or_bank=True).count()
        self.stdout.write(f"Total ledgers now flagged as Cash/Bank: {remaining}")
 