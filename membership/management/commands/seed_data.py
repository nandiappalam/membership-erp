from django.core.management.base import BaseCommand
from membership.models import (
    Organisation,
    AssessmentYear,
    MembershipType,
    FeeMaster,
    PaymentMode,
    AccountGroup,
    Ledger,
)


class Command(BaseCommand):
    help = "Create initial master data"

    def handle(self, *args, **options):

        # ---------------------------------------------------
        # Organisation
        # ---------------------------------------------------
        organisation, _ = Organisation.objects.get_or_create(
            short_name="BVC",
            defaults={
                "organisation_name": "BVC Membership Association",
                "address": "",
                "district": "",
                "state": "Tamil Nadu",
                "country": "India",
                "mobile": "",
                "email": "",
                "website": "",
            },
        )

        # ---------------------------------------------------
        # Assessment Year
        # ---------------------------------------------------
        AssessmentYear.objects.get_or_create(
            organisation=organisation,
            start_year=2026,
            end_year=2027,
            defaults={
                "is_active": True,
            },
        )

        # ---------------------------------------------------
        # Membership Types
        # ---------------------------------------------------
        MembershipType.objects.get_or_create(
            name="Annual",
            defaults={
                "type": "ANNUAL",
                "fee": 1500,
            },
        )

        MembershipType.objects.get_or_create(
            name="Lifetime",
            defaults={
                "type": "LIFETIME",
                "fee": 10000,
            },
        )

        # ---------------------------------------------------
        # Payment Modes
        # ---------------------------------------------------
        for mode in [
            "Cash",
            "Bank",
            "UPI",
            "Cheque",
            "Card",
        ]:
            PaymentMode.objects.get_or_create(
                organisation=organisation,
                name=mode,
            )

        # ---------------------------------------------------
        # Fee Masters
        # ---------------------------------------------------
        fees = [
            ("Membership Fee", "MEMBERSHIP", 1500),
            ("Admission Fee", "ADMISSION", 500),
            ("Renewal Fee", "RENEWAL", 1500),
            ("Identity Card Fee", "IDCARD", 100),
            ("Donation", "DONATION", 0),
        ]

        for name, fee_type, amount in fees:
            FeeMaster.objects.get_or_create(
                organisation=organisation,
                fee_name=name,
                defaults={
                    "fee_type": fee_type,
                    "default_amount": amount,
                },
            )

        # ---------------------------------------------------
        # Account Groups
        # ---------------------------------------------------
        groups = [
            ("Assets", None, "ASSET", 100),
            ("Liabilities", None, "LIABILITY", 200),
            ("Direct Income", None, "DIRECT_INCOME", 300),
            ("Indirect Income", None, "INDIRECT_INCOME", 400),
            ("Direct Expense", None, "DIRECT_EXPENSE", 500),
            ("Indirect Expense", None, "INDIRECT_EXPENSE", 600),
        ]

        group_objects = {}

        for name, parent, nature, prefix in groups:

            obj, _ = AccountGroup.objects.get_or_create(
                name=name,
                defaults={
                    "nature": nature,
                    "code_prefix": prefix,
                    "display_order": prefix,
                    "is_system": True,
                },
            )

            group_objects[name] = obj

        # ---------------------------------------------------
        # Ledgers
        # ---------------------------------------------------
        ledgers = [
            ("100001", "Cash", "Assets"),
            ("100002", "Bank", "Assets"),
            ("300001", "Membership Income", "Direct Income"),
            ("400001", "Donation Income", "Indirect Income"),
        ]

        for code, name, group_name in ledgers:

            Ledger.objects.get_or_create(
                ledger_code=code,
                defaults={
                    "ledger_name": name,
                    "group": group_objects[group_name],
                    "is_system": True,
                },
            )

        self.stdout.write(
            self.style.SUCCESS("Master data created successfully.")
        )