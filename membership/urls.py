from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("organisation/", views.organisation_list, name="organisation_list"),
    path("organisation/add/", views.organisation_create, name="organisation_create"),
    path("organisation/edit/<int:id>/", views.organisation_edit, name="organisation_edit"),
    path("organisation/delete/<int:id>/", views.organisation_delete, name="organisation_delete"),
    
    path("members-type/", views.members_type_list, name="members_type_list"),
    path("members-type/create/", views.members_type_create, name="members_type_create"),
    path("members-type/edit/<int:id>/", views.members_type_edit, name="members_type_edit"),
    path("members-type/delete/<int:id>/", views.members_type_delete, name="members_type_delete"),

    path("members/",views.member_list,name="member_list",),
    path("members/edit/<int:id>/",views.member_edit,name="member_edit",),

    path("fee-master/",views.fee_master_list,name="fee_master_list",),
    path("fee-master/add/",views.fee_master_create,name="fee_master_create",),
    path("fee-master/edit/<int:id>/",views.fee_master_edit,name="fee_master_edit",),
    path("fee-master/delete/<int:id>/",views.fee_master_delete,name="fee_master_delete",),

    path(
    "payment-mode/",
    views.payment_mode_list,
    name="payment_mode_list",
    ),

    path(
        "payment-mode/add/",
        views.payment_mode_create,
        name="payment_mode_create",
    ),

    path(
        "payment-mode/edit/<int:id>/",
        views.payment_mode_edit,
        name="payment_mode_edit",
    ),

    path(
        "payment-mode/delete/<int:id>/",
        views.payment_mode_delete,
        name="payment_mode_delete",
    ),

        path(
        "receipts/",
        views.receipt_list,
        name="receipt_list",
    ),

    path(
        "receipts/add/",
        views.receipt_create,
        name="receipt_create",
    ),

    path(
        "receipts/edit/<int:id>/",
        views.receipt_edit,
        name="receipt_edit",
    ),

    path(
        "receipts/delete/<int:id>/",
        views.receipt_delete,
        name="receipt_delete",
    ),

    path(
        "receipts/print/<int:id>/",
        views.receipt_print,
        name="receipt_print",
    ),

        path("", views.login_view, name="login"),
        path("dashboard/", views.dashboard, name="dashboard"),
        path("logout/", views.logout_view, name="logout"),

    path("users/", views.user_list, name="user_list"),
    path("users/add/", views.user_create, name="user_create"),
    path("users/edit/<int:id>/", views.user_edit, name="user_edit"),
    path("users/delete/<int:id>/", views.user_delete, name="user_delete"),

    path("members/", views.member_list, name="member_list"),
    path("members/add/", views.member_create, name="member_create"),
    path("members/edit/<int:id>/", views.member_edit, name="member_edit"),
    path("members/delete/<int:id>/", views.member_delete, name="member_delete"),
    path("members/view/<int:id>/", views.member_view, name="member_view"),

    path(
    "members/id-card/<int:id>/",
    views.member_id_card,
    name="member_id_card",
),
path(
    "members/id-card-back/<int:id>/",
    views.member_id_card_back,
    name="member_id_card_back",
),

path(
    "members/id-card/print/<int:id>/",
    views.member_id_card_print,
    name="member_id_card_print",
),

  path(
        "members/certificate/<int:pk>/",
        views.member_certificate,
        name="member_certificate",
    ),

# Renewal
path(
    "renewals/",
    views.renewal_list,
    name="renewal_list",
),

path(
    "renewals/create/",
    views.renewal_create,
    name="renewal_create",
),

path(
    "renewals/edit/<int:id>/",
    views.renewal_edit,
    name="renewal_edit",
),

path(
    "renewals/delete/<int:id>/",
    views.renewal_delete,
    name="renewal_delete",
),

path(
    "renewals/print/<int:id>/",
    views.renewal_print,
    name="renewal_print",
),

path(
    "api/member/<int:id>/",
    views.member_api,
    name="member_api",
),

path(
    "report/expiry/",
    views.expiry_report,
    name="expiry_report"
),

path(
    "whatsapp-reminder/",
    views.whatsapp_reminder,
    name="whatsapp_reminder",
),

path(
    "whatsapp-preview/",
    views.whatsapp_preview,
    name="whatsapp_preview",
),

path(
    "whatsapp-next/",
    views.whatsapp_next,
    name="whatsapp_next",
),

path(
    "account-group/",
    views.account_group_list,
    name="accountgroup_list",
),

path(
    "ledger/",
    views.ledger_list,
    name="ledger_list"
),
path(
    "ledger/search/",
    views.ledger_search,
    name="ledger_search",
),

path(
    "ledger/create/",
    views.ledger_create,
    name="ledger_create"
),

path(
    "ledger/edit/<int:id>/",
    views.ledger_edit,
    name="ledger_edit"
),

path(
    "ledger/delete/<int:id>/",
    views.ledger_delete,
    name="ledger_delete"
),

path(
    "voucher/",
    views.voucher_list,
    name="voucher_list",
),

path(
    "voucher/create/",
    views.voucher_create,
    name="voucher_create",
),

path(
    "voucher/edit/<int:id>/",
    views.voucher_edit,
    name="voucher_edit",
),

path(
    "voucher/delete/<int:id>/",
    views.voucher_delete,
    name="voucher_delete",
),


path(
    "get-voucher-number/",
    views.get_voucher_number,
    name="get_voucher_number",
),

path("vouchers/<int:pk>/print/", views.voucher_print, name="voucher_print"),

path(
    "ledger/<int:id>/",
    views.ledger_book,
    name="ledger_book",
),

path(
    "ledger/<int:id>/print/",
    views.ledger_print,
    name="ledger_print",
),

path(
    "ledger/<int:id>/pdf/",
    views.ledger_pdf,
    name="ledger_pdf",
),

path(
    "ledger/<int:id>/excel/",
    views.ledger_excel,
    name="ledger_excel",
),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


