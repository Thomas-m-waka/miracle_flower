import datetime
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Event(models.Model):
    class Status(models.TextChoices):
        UPCOMING = "upcoming", "Upcoming"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(help_text="Full description shown on the event detail page.")
    short_description = models.CharField(
        max_length=200, help_text="Short summary shown on event cards."
    )
    event_date = models.DateField()
    event_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=200)
    featured_image = models.ImageField(upload_to="events/")
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.UPCOMING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-event_date"]
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Event.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("events:detail", kwargs={"slug": self.slug})

    @property
    def is_upcoming(self):
        """Distinguish upcoming vs completed automatically based on date,
        while still respecting an explicit 'cancelled' status."""
        if self.status == self.Status.CANCELLED:
            return False
        if self.status == self.Status.COMPLETED:
            return False
        return self.event_date >= timezone.localdate()

    @property
    def is_past(self):
        return self.event_date < timezone.localdate() or self.status == self.Status.COMPLETED

    @property
    def related_events(self):
        return Event.objects.exclude(pk=self.pk).exclude(
            status=self.Status.CANCELLED
        )[:3]


class EventPhoto(models.Model):
    event = models.ForeignKey(Event, related_name="photos", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="events/gallery/")
    caption = models.CharField(max_length=150, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Event Photo"
        verbose_name_plural = "Event Photos"

    def __str__(self):
        return f"Photo for {self.event.title}"
