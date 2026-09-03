from django.contrib import messages
from django.shortcuts import redirect, render

from events.models import Event, EventPhoto
from flowers.models import Flower

from .forms import ContactMessageForm
from .models import AboutFeature, SiteSettings


def home(request):
    site = SiteSettings.get_active()
    featured_count = site.featured_flowers_count if site else 6

    featured_flowers = Flower.objects.filter(
        available=True, featured=True
    ).select_related("category")[:featured_count]

    upcoming_events = Event.objects.filter(
        status=Event.Status.UPCOMING
    ).order_by("event_date")[:3]

    recent_photos = EventPhoto.objects.select_related("event").order_by(
        "-uploaded_at"
    )[:6]

    context = {
        "page_title": "Home",
        "featured_flowers": featured_flowers,
        "upcoming_events": upcoming_events,
        "recent_photos": recent_photos,
    }
    return render(request, "home.html", context)


def gallery(request):
    photos = EventPhoto.objects.select_related("event").order_by("-uploaded_at")
    flowers_with_extra_images = Flower.objects.filter(
        available=True, images__isnull=False
    ).distinct().prefetch_related("images")

    context = {
        "page_title": "Gallery",
        "photos": photos,
        "flowers_with_extra_images": flowers_with_extra_images,
    }
    return render(request, "gallery.html", context)


def about(request):
    features = AboutFeature.objects.all()
    context = {
        "page_title": "About Us",
        "features": features,
    }
    return render(request, "about.html", context)


def contact(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thank you! Your message has been sent. We'll get back to you soon.",
            )
            return redirect("core:contact")
    else:
        initial = {}
        prefill_subject = request.GET.get("subject")
        if prefill_subject:
            initial["subject"] = prefill_subject
        form = ContactMessageForm(initial=initial)

    context = {
        "page_title": "Contact Us",
        "form": form,
    }
    return render(request, "contact.html", context)


def error_404(request, exception=None):
    return render(request, "404.html", status=404)


def error_500(request):
    return render(request, "500.html", status=500)
