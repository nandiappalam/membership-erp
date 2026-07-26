from django.db import models
from django.utils.text import slugify

from membership.models import  *
import qrcode
from io import BytesIO
from django.core.files import File

class Event(models.Model):
    EVENT_TYPES = (
        ("AGM", "AGM"),
        ("SEMINAR", "Seminar"),
        ("TRAINING", "Training"),
        ("EXPO", "Expo"),
        ("MEETING", "Meeting"),
        ("OTHER", "Other"),
    )

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        default="AGM",
    )

    STATUS = (
        ("OPEN", "Open"),
        ("CLOSED", "Closed"),
        ("CANCELLED", "Cancelled"),
    )

    event_code = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    event_name = models.CharField(max_length=200)

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE
    )

    assessment_year = models.ForeignKey(
        AssessmentYear,
        on_delete=models.CASCADE
    )

    event_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    venue = models.CharField(max_length=250)

    description = models.TextField(blank=True)

    registration_open = models.BooleanField(default=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="OPEN"
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    
    qr_enabled = models.BooleanField(default=True)
    gift_coupon = models.BooleanField(default=True)
    lucky_draw = models.BooleanField(default=True)
    max_participants = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-event_date", "-id"]

    def save(self, *args, **kwargs):

        if not self.event_code:
            last = Event.objects.order_by("-id").first()

            if last:
                number = int(last.event_code.replace("EV", "")) + 1
            else:
                number = 1

            self.event_code = f"EV{number:05d}"

        if not self.slug:
            self.slug = slugify(f"{self.event_code}-{self.event_name}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.event_code} - {self.event_name}"


class EventAttendance(models.Model):

    ENTRY_TYPES = (
        ("MEMBER", "Member"),
        ("VISITOR", "Visitor"),
    )

    CHECKIN_METHODS = (
        ("QR", "QR Scan"),
        ("MANUAL", "Manual Entry"),
        ("ADMIN", "Admin Entry"),
    )

    STATUS = (
        ("PRESENT", "Present"),
        ("CANCELLED", "Cancelled"),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="PRESENT",
    )

    
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="attendances"
    )

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    entry_type = models.CharField(
        max_length=10,
        choices=ENTRY_TYPES,
        default="MEMBER"
    )

    checkin_method = models.CharField(
        max_length=10,
        choices=CHECKIN_METHODS,
        default="QR"
    )

    check_in_time = models.DateTimeField(
        auto_now_add=True
    )

    coupon_issued = models.BooleanField(
        default=False
    )

    remarks = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ["-check_in_time"]

        constraints = [
            models.UniqueConstraint(
                fields=["event", "member"],
                name="unique_member_attendance_per_event"
            )
        ]

    def __str__(self):
        if self.member:
            return f"{self.member.membership_no} - {self.member.owner_name}"
        return f"Attendance #{self.id}"


class EventVisitor(models.Model):

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="visitors"
    )

    visitor_name = models.CharField(
        max_length=200
    )

    mobile = models.CharField(
        max_length=15
    )

    company = models.CharField(
        max_length=200,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    referred_by = models.ForeignKey(
        Member,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,  
    )
    attendance = models.OneToOneField(
        EventAttendance,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["event", "mobile"],
                name="unique_visitor_mobile_per_event"
            )
        ]

    def __str__(self):
        return self.visitor_name


class EventCoupon(models.Model):

    coupon_no = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="coupons"
    )

    attendance = models.OneToOneField(
        EventAttendance,
        on_delete=models.CASCADE,
        related_name="coupon"
    )

    lucky_draw_no = models.PositiveIntegerField(
        default=0
    )

    qr_code = models.ImageField(
        upload_to="coupon_qr/",
        blank=True,
        null=True
    )

    printed = models.BooleanField(default=False)

    is_winner = models.BooleanField(default=False)

    prize_name = models.CharField(
        max_length=200,
        blank=True
    )

    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["coupon_no"]

    def save(self, *args, **kwargs):

        # Coupon Number
        if not self.coupon_no:

            last = EventCoupon.objects.order_by("-id").first()

            if last:
                number = int(last.coupon_no.replace("CP", "")) + 1
            else:
                number = 1

            self.coupon_no = f"CP{number:06d}"

        # Lucky Draw Number
        if self.lucky_draw_no == 0:

            last = EventCoupon.objects.order_by("-lucky_draw_no").first()

            if last:
                self.lucky_draw_no = last.lucky_draw_no + 1
            else:
                self.lucky_draw_no = 1

        if not self.lucky_draw_no:
            self.lucky_draw_no = (
                EventCoupon.objects.filter(event=self.event).count() + 1
            )

        super().save(*args, **kwargs)

        if not self.qr_code:

            qr = qrcode.make(
                f"""
        Coupon : {self.coupon_no}
        Lucky Draw : {self.lucky_draw_no}
        Member : {self.attendance.member.owner_name}
        Membership : {self.attendance.member.membership_no}
        Event : {self.event.event_name}
        """
            )

            buffer = BytesIO()

            qr.save(buffer, format="PNG")

            self.qr_code.save(
                f"{self.coupon_no}.png",
                File(buffer),
                save=False
            )

            super().save(update_fields=["qr_code"])

    def __str__(self):
        return self.coupon_no

    

class EventPrize(models.Model):

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="prizes"
    )

    prize_name = models.CharField(
        max_length=200
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    sponsor = models.CharField(
        max_length=200,
        blank=True
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["prize_name"]

    def __str__(self):
        return self.prize_name

    

class EventWinner(models.Model):

    coupon = models.OneToOneField(
        EventCoupon,
        on_delete=models.CASCADE,
        related_name="winner"
    )

    prize = models.ForeignKey(
        EventPrize,
        on_delete=models.CASCADE
    )

    declared_at = models.DateTimeField(
        auto_now_add=True
    )

    remarks = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.coupon.coupon_no} - {self.prize.prize_name}"


