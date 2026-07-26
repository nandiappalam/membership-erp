from django.db import transaction

from .models import Voucher
from .models import *


@transaction.atomic
def create_receipt_voucher(receipt, user):

    print("=" * 50)
    print("INSIDE create_receipt_voucher()")
    print("Receipt:", receipt.receipt_no)
    print("=" * 50)

    last = Voucher.objects.order_by("-id").first()

    next_no = last.id + 1 if last else 1

    voucher = Voucher.objects.create(
        voucher_no=f"RV{next_no:05d}",
        voucher_type="RV",
        voucher_date=receipt.receipt_date,
        narration=f"Receipt No {receipt.receipt_no}",
        reference_no=str(receipt.receipt_no),
        created_by=user,
    )

    payment_ledger = receipt.payment_mode.ledger

    if payment_ledger is None:
        raise Exception(
            f"Payment Mode '{receipt.payment_mode.name}' has no ledger assigned."
        )

    # Debit Cash / Bank
    VoucherEntry.objects.create(
        voucher=voucher,
        ledger=receipt.payment_mode.ledger,
        debit=receipt.total_amount,
        credit=0,
        entry_type="Dr",
    )

    # Credit each fee separately
    for detail in receipt.details.select_related("fee_master__ledger"):

        if not detail.fee_master.ledger:
            raise Exception(
                f"Ledger not assigned for {detail.fee_master.fee_name}"
            )

        VoucherEntry.objects.create(
            voucher=voucher,
            ledger=detail.fee_master.ledger,
            debit=0,
            credit=detail.amount,
            entry_type="Cr",
        )

    print("Voucher Created:", voucher.id, voucher.voucher_no)

    return voucher

