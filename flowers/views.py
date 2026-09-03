from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from .models import Flower, FlowerCategory



def catalog(request):
    flowers = (
        Flower.objects
        .select_related("category")
        .order_by("-created_at")
    )
    category_slug = request.GET.get("category")

    active_category = None

    if category_slug:
        active_category = (
            FlowerCategory.objects
            .filter(slug=category_slug)
            .first()
        )

        if active_category:
            flowers = flowers.filter(category=active_category)

    availability = request.GET.get("availability")

    if availability == "available":
        flowers = flowers.filter(available=True)

    elif availability == "unavailable":
        flowers = flowers.filter(available=False)
    paginator = Paginator(flowers, 12)

    page_number = request.GET.get("page", 1)

    page_obj = paginator.get_page(page_number)
    categories = FlowerCategory.objects.order_by("name")
    context = {
        "page_title": "Our Flowers",
        "page_obj": page_obj,
        "flowers": page_obj.object_list,
        "categories": categories,
        "active_category": active_category,
        "active_availability": availability or "",        
        "flower_count": paginator.count,
    }

    return render(
        request,
        "flowers/catalog.html",
        context
    )


def detail(request, slug):
    flower = get_object_or_404(
        Flower.objects.select_related("category").prefetch_related("images"),
        slug=slug,
    )
    context = {
        "page_title": flower.name,
        "flower": flower,
        "related_flowers": flower.related_flowers,
    }
    return render(request, "flowers/detail.html", context)
