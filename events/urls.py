from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.event_list,
        name="event_list",
    ),

    path(
        "add/",
        views.event_create,
        name="event_create",
    ),

    path(
        "edit/<int:id>/",
        views.event_edit,
        name="event_edit",
    ),

    path(
        "delete/<int:id>/",
        views.event_delete,
        name="event_delete",
    ),

    path(
    "attendance/",
    views.attendance_list,
    name="attendance_list",
),

path(
    "attendance/add/",
    views.attendance_add,
    name="attendance_add",
),

path(
    "attendance/save/",
    views.attendance_save,
    name="attendance_save",
),

path(
    "api/member-search/",
    views.search_member,
    name="search_member",
),

path(
    "coupon/<int:id>/print/",
    views.coupon_print,
    name="coupon_print",
),



path(
    "agm-entry/<int:event_id>/",
    views.agm_entry,
    name="agm_entry"
),

path(
    "visitor-save/<int:event_id>/",
    views.visitor_save,
    name="visitor_save"
),

path(
    "qr/<int:id>/",
    views.event_qr_print,
    name="event_qr_print",
),


path(
    "print-queue/",
    views.print_queue,
    name="print_queue",
),


path(
    "visitor-pass/<int:id>/print/",
    views.visitor_pass_print,
    name="visitor_pass_print",
),

path(
    "reports/",
    views.agm_reports,
    name="agm_reports",
),

path(
    "reports/members/",
    views.member_attendance_report,
    name="member_attendance_report",
),


path(
    "reports/visitors/",
    views.visitor_report,
    name="visitor_report",
),

path(
    "reports/members/print/",
    views.member_attendance_print,
    name="member_attendance_print",
),

path(
    "reports/visitors/print/",
    views.visitor_report_print,
    name="visitor_report_print",
),



]