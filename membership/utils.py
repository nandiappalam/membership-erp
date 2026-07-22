from datetime import date
from .models import *
def get_current_assessment_year():
    today = date.today()

    if today.month >= 4:
        start_year = today.year
        end_year = today.year + 1
    else:
        start_year = today.year - 1
        end_year = today.year

    return start_year, end_year

def get_next_voucher_no(voucher_type):

    prefix = {
        "RV": "RV",
        "PV": "PV",
        "JV": "JV",
        "CV": "CV",
    }.get(voucher_type, "VT")

    last = (
        Voucher.objects
        .filter(voucher_type=voucher_type)
        .order_by("-id")
        .first()
    )

    if last:

        number = int(last.voucher_no[2:]) + 1

    else:

        number = 1

    return f"{prefix}{number:06d}"