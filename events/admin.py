from django.contrib import admin
from .models import *


admin.site.register(Event)
admin.site.register(EventAttendance)
admin.site.register(EventCoupon)
admin.site.register(EventPrize)
admin.site.register(EventWinner)
class EventAdmin(admin.ModelAdmin):

    list_display = (
        "event_code",
        "event_name",
        "event_date",
        "venue",
        "status",
        "registration_open",
    )

    search_fields = (
        "event_code",
        "event_name",
        "venue",
    )

    list_filter = (
        "status",
        "event_date",
        "organisation",
    )

    ordering = ("-event_date",)