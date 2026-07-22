from django.contrib import admin
from .models import *
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "role",
        "mobile",
        "is_active",
    )

    list_filter = (
        "role",
        "is_active",
    )

    search_fields = (
        "user__username",
    )


@admin.register(MembershipType)
class MembershipTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "fee")
    search_fields = ("name",)


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


class MemberDocumentInline(admin.TabularInline):
    model = MemberDocument
    extra = 1


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "member_no",
        "owner_name",
        "company_name",
        "mobile",
        "status",
    )






@admin.register(MemberDocument)
class MemberDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "document_type",
        "document_number",
        "expiry_date",
    )

    search_fields = (
    "document_number",
    "member__owner_name",
    "member__company_name",
)

    list_filter = (
        "document_type",
        "expiry_date",
    )

@admin.register(AssessmentYear)
class AssessmentYearAdmin(admin.ModelAdmin):

    list_display = (
        "organisation",
        "start_year",
        "end_year",
        "is_active",
    )

    list_filter = (
        "organisation",
        "is_active",
    )

    search_fields = (
        "organisation__organisation_name",
    )

    @admin.register(Organisation)
    class OrganisationAdmin(admin.ModelAdmin):
        list_display = (
            "organisation_name",
            "short_name",
            "mobile",
        )

        search_fields = (
            "organisation_name",
            "short_name",
        )
admin.site.register(MemberRenewal)

