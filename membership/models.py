from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
from django.utils import timezone
class Organisation(models.Model):
    organisation_name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50)

    address = models.TextField(blank=True)
    district = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default="India")

    mobile = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    pan_no = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    gst_no = models.CharField(
    max_length=20,
    blank=True,
    null=True,
)
    
    registration_no = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    logo = models.ImageField(
        upload_to="organisation/logo/",
        blank=True,
        null=True,
    )


    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.organisation_name

class UserProfile(models.Model):

    ROLE_CHOICES = (
        ("SUPER_ADMIN", "Super Admin"),
        ("ADMIN", "Admin"),
        ("USER", "User"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="USER"
    )

    mobile = models.CharField(max_length=15, blank=True)

    photo = models.ImageField(
        upload_to="users/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

class AssessmentYear(models.Model):

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE
    )

    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_year"]

    def __str__(self):
        return f"{self.start_year}-{self.end_year}"

class MembershipType(models.Model):

    TYPE_CHOICES = (
        ("ANNUAL", "Annual"),
        ("LIFETIME", "Lifetime"),
    )

    name = models.CharField(max_length=100)

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="ANNUAL",
    )

    fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Member(models.Model):
    """
    MEMBERSHIP_TYPES = (
        ("REGULAR", "Regular"),
        ("ASSOCIATE", "Associate"),
        ("LIFE", "Life Member"),
        ("HONORARY", "Honorary"),
    )
    """
    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
        ("SUSPENDED", "Suspended"),
    )

    # =========================
    # Membership
    # =========================
    member_no = models.PositiveIntegerField(unique=True)
    membership_no = models.CharField(max_length=50, unique=True)

    joining_date = models.DateField()
    membership_valid_upto = models.DateField()
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
    )

    assessment_year = models.ForeignKey(
    AssessmentYear,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
)
    
    membership_type = models.ForeignKey(
    MembershipType,
    on_delete=models.PROTECT
)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )

    # =========================
    # Personal
    # =========================
    owner_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    brand_name = models.CharField(max_length=200, blank=True)

    photo = models.ImageField(upload_to="members/photos/", blank=True)
    company_logo = models.ImageField(upload_to="members/logo/", blank=True)

    # =========================
    # Contact
    # =========================
    mobile = models.CharField(max_length=15)
    whatsapp = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)

    website = models.URLField(blank=True)

    # =========================
    # Address
    # =========================
    address = models.TextField()

    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )
    qr_code = models.ImageField(
        upload_to="members/qrcode/",
        blank=True,
        null=True,
    )
    # =========================
    # Documents
    # =========================
    gst_no = models.CharField(max_length=30, blank=True)
    fssai_no = models.CharField(max_length=30, blank=True)
    udyam_no = models.CharField(max_length=30, blank=True)
    factory_license_no = models.CharField(max_length=30, blank=True)
    do_license_no = models.CharField(max_length=30, blank=True)
    trade_license_no = models.CharField(max_length=30, blank=True)
    fire_noc_no = models.CharField(max_length=30, blank=True)
    pollution_no = models.CharField(max_length=30, blank=True)

    # =========================
    # Remarks
    # =========================
    remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        qr_data = (
            f"Member No : {self.membership_no}\n"
            f"Name : {self.owner_name}\n"
            f"Company : {self.company_name}\n"
            f"Organisation : {self.organisation.organisation_name}\n"
            f"Mobile : {self.mobile}\n"
            f"Valid Upto : {self.membership_valid_upto}"
        )

        qr = qrcode.make(qr_data)

        canvas = BytesIO()

        qr.save(canvas, format="PNG")

        filename = f"{self.membership_no}.png"

        self.qr_code.save(
            filename,
            File(canvas),
            save=False,
        )

        canvas.close()

        super().save(update_fields=["qr_code"])

    def __str__(self):
        return f"{self.member_no} - {self.company_name}"


    

class DocumentType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MemberDocument(models.Model):

    DOCUMENT_TYPES = (
        ("GST", "GST"),
        ("FSSAI", "FSSAI"),
        ("UDYAM", "UDYAM"),
        ("FACTORY", "Factory License"),
        ("DO", "DO License"),
        ("TRADE", "Trade License"),
        ("FIRE", "Fire NOC"),
        ("POLLUTION", "Pollution Certificate"),
        ("OTHER", "Other"),
    )

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_number = models.CharField(max_length=100)

    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)

    document_file = models.FileField(upload_to="member_documents/")

    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.member.company_name} - {self.document_type}"



class FeeMaster(models.Model):
    FEE_TYPES = [
        ("MEMBERSHIP", "Membership Fee"),
        ("ADMISSION", "Admission Fee"),
        ("RENEWAL", "Renewal Fee"),
        ("IDCARD", "Identity Card Fee"),
        ("LATE", "Late Fee"),
        ("DONATION", "Donation"),
        ("BUILDING", "Building Fund"),
        ("WELFARE", "Welfare Fund"),
        ("EVENT", "Event Fee"),
        ("OTHER", "Other"),
    ]

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE
    )

    fee_name = models.CharField(max_length=100)

    fee_type = models.CharField(
        max_length=20,
        choices=FEE_TYPES,
        default="OTHER",
    )

    default_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fee_name"]

    def __str__(self):
        return self.fee_name
    

class PaymentMode(models.Model):
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=50)

    description = models.TextField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        unique_together = ("organisation", "name")

    def __str__(self):
        return self.name
    
class Receipt(models.Model):

    receipt_no = models.PositiveIntegerField()

    receipt_date = models.DateField()

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE
    )

    assessment_year = models.ForeignKey(
        AssessmentYear,
        on_delete=models.CASCADE
    )

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE
    )

    payment_mode = models.ForeignKey(
        PaymentMode,
        on_delete=models.PROTECT
    )

    reference_no = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-receipt_date", "-receipt_no"]

    def __str__(self):
        return f"Receipt {self.receipt_no}"
    
class ReceiptDetail(models.Model):

    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name="details"
    )

    fee_master = models.ForeignKey(
        FeeMaster,
        on_delete=models.PROTECT
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return self.fee_master.fee_name
    
class MemberRenewal(models.Model):

    PAYMENT_CHOICES = (
        ("Cash", "Cash"),
        ("UPI", "UPI"),
        ("Card", "Card"),
        ("Cheque", "Cheque"),
        ("Bank", "Bank"),
    )

    renewal_no = models.CharField(max_length=20, unique=True)

    member = models.ForeignKey(
        "Member",
        on_delete=models.CASCADE,
        related_name="renewals"
    )

    renewal_date = models.DateField()

    previous_valid_upto = models.DateField()

    new_valid_upto = models.DateField()

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="Cash"
    )

    receipt = models.ForeignKey(
        "Receipt",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    assessment_year = models.ForeignKey(
        AssessmentYear,
        on_delete=models.PROTECT,
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-renewal_date"]

    def __str__(self):
        return self.renewal_no
    
class AccountGroup(models.Model):

    GROUP_TYPES = (
        ("ASSET", "Asset"),
        ("LIABILITY", "Liability"),
        ("DIRECT_INCOME", "Direct Income"),
        ("INDIRECT_INCOME", "Indirect Income"),
        ("DIRECT_EXPENSE", "Direct Expense"),
        ("INDIRECT_EXPENSE", "Indirect Expense"),
    )

    name = models.CharField(
        max_length=100,
        unique=True
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children"
    )

    nature = models.CharField(
        max_length=20,
        choices=GROUP_TYPES
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    is_system = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    code_prefix = models.PositiveIntegerField(
    unique=True,
    null=True,
    blank=True
)
    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Account Group"
        verbose_name_plural = "Account Groups"

    def __str__(self):
        return self.name
    

class Ledger(models.Model):

    OPENING_TYPE = (
        ("DEBIT", "Debit"),
        ("CREDIT", "Credit"),
    )

    ledger_code = models.CharField(
        max_length=20,
        unique=True
    )

    ledger_name = models.CharField(
        max_length=100,
        unique=True
    )

    group = models.ForeignKey(
        AccountGroup,
        on_delete=models.PROTECT,
        related_name="ledgers"
    )

    opening_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    opening_type = models.CharField(
        max_length=10,
        choices=OPENING_TYPE,
        default="DEBIT"
    )

    remarks = models.TextField(
        blank=True
    )

    is_system = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:
        ordering = ["ledger_code"]


    def __str__(self):
        return self.ledger_name   
    
class Voucher(models.Model):

    VOUCHER_TYPES = (
        ("RV", "Receipt Voucher"),
        ("PV", "Payment Voucher"),
        ("JV", "Journal Voucher"),
        ("CV", "Contra Voucher"),
    )

    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("CANCELLED", "Cancelled"),
    )

    voucher_no = models.CharField(
        max_length=20,
        unique=True
    )

    voucher_type = models.CharField(
        max_length=2,
        choices=VOUCHER_TYPES
    )

    voucher_date = models.DateField()

    narration = models.TextField(
        blank=True,
        null=True
    )

    reference_no = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-voucher_date", "-id"]

    def __str__(self):
        return self.voucher_no
    

class VoucherEntry(models.Model):

    voucher = models.ForeignKey(
        Voucher,
        on_delete=models.CASCADE,
        related_name="entries"
    )

    ledger = models.ForeignKey(
        Ledger,
        on_delete=models.PROTECT
    )

    debit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    credit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    narration = models.CharField(
        max_length=250,
        blank=True,
        null=True
    )

    entry_type = models.CharField(
        max_length=2,
        choices=(
            ("Dr","Debit"),
            ("Cr","Credit"),
        ),
        default="Dr"
    )


    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.voucher.voucher_no} - {self.ledger.ledger_name}"
    
