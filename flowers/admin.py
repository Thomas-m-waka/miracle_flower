from django.contrib import admin
from django.utils.html import format_html

from .models import Flower, FlowerCategory, FlowerImage


class FlowerImageInline(admin.TabularInline):
    model = FlowerImage
    extra = 1
    fields = ("image", "caption", "order", "preview")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:6px;" />', obj.image.url)
        return "—"
    preview.short_description = "Preview"


@admin.register(FlowerCategory)
class FlowerCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "flower_count", "created_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)

    def flower_count(self, obj):
        return obj.flowers.count()
    flower_count.short_description = "Flowers"


@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = (
        "name", "category", "price", "available", "featured",
        "image_preview", "updated_at",
    )
    list_filter = ("available", "featured", "category")
    search_fields = ("name", "description", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("available", "featured")
    readonly_fields = ("created_at", "updated_at", "image_preview")
    inlines = [FlowerImageInline]
    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "slug", "category", "short_description", "description"),
        }),
        ("Pricing & Availability", {
            "fields": ("price", "available", "featured"),
        }),
        ("Media", {
            "fields": ("main_image", "image_preview"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    def image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="height:80px;border-radius:8px;" />', obj.main_image.url)
        return "No image"
    image_preview.short_description = "Preview"
