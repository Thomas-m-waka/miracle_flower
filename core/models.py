from django.core.exceptions import ValidationError
from django.db import models


class SiteSettings(models.Model):
    business_name = models.CharField(max_length=150, default="Miracle Flowers")
    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    hero_image = models.ImageField(upload_to="site/", blank=True, null=True)
    hero_tagline = models.CharField(
        max_length=200,
        default="Beautiful flowers for life's beautiful moments.",
    )
    hero_subtext = models.TextField(
        default=(
            "Miracle Flowers provides beautiful floral arrangements for "
            "celebrations, special occasions, events, and everyday moments."
        )
    )

    phone_number = models.CharField(max_length=30, default="+254 700 000 000")
    email = models.EmailField(default="hello@miracleflowers.co.ke")
    address = models.CharField(
        max_length=255, default="Argwings Kodhek Road, Nairobi, Kenya"
    )
    opening_hours = models.CharField(
        max_length=255, default="Mon – Sat: 8:00 AM – 7:00 PM, Sun: 10:00 AM – 4:00 PM"
    )

    featured_flowers_count = models.PositiveIntegerField(
        default=6,
        help_text="How many flowers to show in the homepage 'Featured Flowers' section.",
    )

    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)

    about_text = models.TextField(
        default=(
            "Miracle Flowers began with a simple belief: that flowers have "
            "the power to turn ordinary moments into unforgettable ones. "
            "From weddings and graduations to a quiet Tuesday that deserves "
            "a little brightness, our florists hand-craft every arrangement "
            "with care, freshness, and an eye for detail."
        )
    )
    mission_text = models.TextField(
        default=(
            "Our mission is to deliver fresh, thoughtfully designed floral "
            "arrangements and unforgettable event experiences that help our "
            "customers celebrate life's most meaningful moments."
        )
    )
    footer_text = models.CharField(
        max_length=255,
        default="Premium flowers and floral experiences for every occasion.",
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Only one SiteSettings record should be active at a time.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.business_name

    def clean(self):
        if self.is_active:
            qs = SiteSettings.objects.filter(is_active=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError()

    @classmethod
    def get_active(cls):
        return cls.objects.filter(is_active=True).first() or cls.objects.first()


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.subject} — {self.name}"


class AboutFeature(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Optional short label/emoji used as a simple icon, e.g. '✿'.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "About Feature"
        verbose_name_plural = "About Features"

    def __str__(self):
        return self.title
