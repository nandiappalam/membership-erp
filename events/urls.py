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
    "coupon/<int:id>/print/",
    views.print_coupon,
    name="print_coupon"
),




]