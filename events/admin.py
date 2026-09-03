from django.contrib import admin
from django.utils.html import format_html

from .models import Event, EventPhoto


class EventPhotoInline(admin.TabularInline):
    model = EventPhoto
    extra = 1
    fields = ("image", "caption", "preview")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:6px;" />', obj.image.url)
        return "—"
    preview.short_description = "Preview"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title", "event_date", "event_time", "location", "status",
        "is_upcoming", "image_preview",
    )
    list_filter = ("status", "event_date")
    search_fields = ("title", "description", "location")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("status",)
    date_hierarchy = "event_date"
    readonly_fields = ("created_at", "updated_at", "image_preview")
    inlines = [EventPhotoInline]
    fieldsets = (
        ("Event Details", {
            "fields": ("title", "slug", "short_description", "description"),
        }),
        ("Schedule & Location", {
            "fields": ("event_date", "event_time", "location", "status"),
        }),
        ("Media", {
            "fields": ("featured_image", "image_preview"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    def is_upcoming(self, obj):
        return obj.is_upcoming
    is_upcoming.boolean = True
    is_upcoming.short_description = "Upcoming?"

    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="height:80px;border-radius:8px;" />', obj.featured_image.url)
        return "No image"
    image_preview.short_description = "Preview"


@admin.register(EventPhoto)
class EventPhotoAdmin(admin.ModelAdmin):
    list_display = ("event", "caption", "uploaded_at", "image_preview")
    list_filter = ("event",)
    search_fields = ("caption", "event__title")
    readonly_fields = ("uploaded_at", "image_preview")

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:80px;border-radius:8px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"
