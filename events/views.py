from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Event


def event_list(request):
    today = timezone.localdate()

    upcoming_events = Event.objects.filter(
        event_date__gte=today
    ).exclude(status=Event.Status.CANCELLED).order_by("event_date")

    recent_events_qs = Event.objects.filter(
        event_date__lt=today
    ).exclude(status=Event.Status.CANCELLED).order_by("-event_date")

    paginator = Paginator(recent_events_qs, 9)
    page_number = request.GET.get("page")
    recent_page = paginator.get_page(page_number)

    context = {
        "page_title": "Events",
        "upcoming_events": upcoming_events,
        "recent_page": recent_page,
        "recent_events": recent_page.object_list,
    }
    return render(request, "events/event_list.html", context)


def event_detail(request, slug):
    event = get_object_or_404(Event.objects.prefetch_related("photos"), slug=slug)
    context = {
        "page_title": event.title,
        "event": event,
        "related_events": event.related_events,
    }
    return render(request, "events/event_detail.html", context)
