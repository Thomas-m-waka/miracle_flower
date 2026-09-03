from django.contrib import admin
from django.utils.html import format_html

from .models import AboutFeature, ContactMessage, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("business_name", "phone_number", "email", "is_active", "updated_at")
    list_filter = ("is_active",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Identity", {
            "fields": ("business_name", "logo", "hero_image", "hero_tagline", "hero_subtext", "is_active"),
        }),
        ("Homepage Settings", {
            "fields": ("featured_flowers_count",),
        }),
        ("Contact Information", {
            "fields": ("phone_number", "email", "address", "opening_hours"),
        }),
        ("Social Media", {
            "fields": ("facebook_url", "instagram_url", "whatsapp_number"),
        }),
        ("About & Footer Content", {
            "fields": ("about_text", "mission_text", "footer_text"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


@admin.register(AboutFeature)
class AboutFeatureAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "icon", "order")
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "name", "email", "phone", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    list_editable = ("is_read",)
    readonly_fields = ("name", "email", "phone", "subject", "message", "created_at")
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False
