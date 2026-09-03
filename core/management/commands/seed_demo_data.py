"""
Management command: seed_demo_data

Populates the database with realistic demonstration content for
Miracle Flowers: flower categories, flowers, upcoming/completed events,
event photos, about-page features, and site settings.

Placeholder images are generated locally with Pillow so the command
never depends on external image URLs.

Usage:
    python manage.py seed_demo_data
    python manage.py seed_demo_data --flush   # clear existing demo data first
"""

import datetime
import io
import random

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import AboutFeature, SiteSettings
from events.models import Event, EventPhoto
from flowers.models import Flower, FlowerCategory, FlowerImage

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    Image = None


PALETTE = [
    ("#E7B8B4", "#1E3D2B"),
    ("#B4894F", "#FBF7EF"),
    ("#2F5540", "#FBF7EF"),
    ("#1E3D2B", "#E7B8B4"),
    ("#CF8F8A", "#FBF7EF"),
    ("#F2E9D8", "#1E3D2B"),
]


def make_placeholder_image(label, size=(900, 700), seed=None):
    """Generate a simple, tasteful placeholder image with a label."""
    if Image is None:
        raise RuntimeError("Pillow is required to generate placeholder images.")

    rnd = random.Random(seed or label)
    bg_hex, fg_hex = rnd.choice(PALETTE)

    img = Image.new("RGB", size, bg_hex)
    draw = ImageDraw.Draw(img)

    # A few soft overlapping circles to suggest a floral motif.
    for _ in range(5):
        r = rnd.randint(60, 160)
        cx = rnd.randint(0, size[0])
        cy = rnd.randint(0, size[1])
        overlay_color = rnd.choice(PALETTE)[0]
        draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            fill=overlay_color,
        )

    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34
        )
    except Exception:
        font = ImageFont.load_default()

    text = label
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.rectangle(
        [
            (size[0] - tw) / 2 - 20,
            (size[1] - th) / 2 - 14,
            (size[0] + tw) / 2 + 20,
            (size[1] + th) / 2 + 14,
        ],
        fill=fg_hex,
    )
    draw.text(
        ((size[0] - tw) / 2, (size[1] - th) / 2 - bbox[1]),
        text,
        font=font,
        fill=bg_hex,
    )

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    buffer.seek(0)
    return ContentFile(buffer.read(), name=f"{label.lower().replace(' ', '-')}.jpg")


class Command(BaseCommand):
    help = "Populate the database with realistic Miracle Flowers demo data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing flowers, events, and related data before seeding.",
        )

    def handle(self, *args, **options):
        if Image is None:
            self.stderr.write(
                self.style.ERROR(
                    "Pillow is not installed. Run: pip install Pillow --break-system-packages"
                )
            )
            return

        if options["flush"]:
            self.stdout.write("Flushing existing demo data...")
            EventPhoto.objects.all().delete()
            Event.objects.all().delete()
            FlowerImage.objects.all().delete()
            Flower.objects.all().delete()
            FlowerCategory.objects.all().delete()
            AboutFeature.objects.all().delete()

        self._seed_site_settings()
        self._seed_about_features()
        categories = self._seed_categories()
        self._seed_flowers(categories)
        self._seed_events()

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))

    def _seed_site_settings(self):
        if SiteSettings.objects.filter(is_active=True).exists():
            self.stdout.write("Active SiteSettings already exists — skipping.")
            return
        settings_obj = SiteSettings.objects.create(
            business_name="Miracle Flowers",
            hero_tagline="Beautiful flowers for life's beautiful moments.",
            hero_subtext=(
                "Miracle Flowers provides beautiful floral arrangements for "
                "celebrations, special occasions, events, and everyday moments."
            ),
            phone_number="+254 700 123 456",
            email="hello@miracleflowers.co.ke",
            address="Argwings Kodhek Road, Nairobi, Kenya",
            opening_hours="Mon – Sat: 8:00 AM – 7:00 PM, Sun: 10:00 AM – 4:00 PM",
            facebook_url="https://facebook.com/miracleflowers",
            instagram_url="https://instagram.com/miracleflowers",
            whatsapp_number="254700123456",
            featured_flowers_count=6,
            is_active=True,
        )
        settings_obj.hero_image.save(
            "hero.jpg", make_placeholder_image("Miracle Flowers", seed="hero"), save=True
        )
        self.stdout.write(self.style.SUCCESS("Created SiteSettings."))

    def _seed_about_features(self):
        if AboutFeature.objects.exists():
            return
        features = [
            ("✿", "Fresh & Beautiful Flowers", "Sourced regularly to keep every arrangement vibrant and long-lasting."),
            ("✎", "Creative Arrangements", "Thoughtful designs tailored to your occasion and personal style."),
            ("♥", "Reliable Service", "Consistent quality and clear communication from enquiry to delivery."),
            ("★", "Special Event Expertise", "Weddings, corporate events, and celebrations styled with care."),
            ("◈", "Attention to Detail", "Every stem, ribbon, and arrangement finished with precision."),
        ]
        for order, (icon, title, desc) in enumerate(features):
            AboutFeature.objects.create(icon=icon, title=title, description=desc, order=order)
        self.stdout.write(self.style.SUCCESS(f"Created {len(features)} about features."))

    def _seed_categories(self):
        if FlowerCategory.objects.exists():
            return list(FlowerCategory.objects.all())

        names = [
            ("Roses", "Classic, romantic roses in a range of colors."),
            ("Bouquets", "Hand-tied bouquets for every occasion."),
            ("Wedding Flowers", "Elegant arrangements for your special day."),
            ("Birthday Flowers", "Bright, cheerful flowers to celebrate another year."),
            ("Anniversary Flowers", "Timeless arrangements to mark a milestone."),
            ("Graduation Flowers", "Congratulatory bouquets for the graduate in your life."),
            ("Event Flowers", "Statement arrangements for corporate and social events."),
            ("Gift Flowers", "Thoughtful flowers for any gifting occasion."),
        ]
        categories = []
        for name, desc in names:
            cat = FlowerCategory.objects.create(name=name, description=desc)
            cat.image.save(
                f"{cat.slug}.jpg",
                make_placeholder_image(name, seed=name),
                save=True,
            )
            categories.append(cat)
        self.stdout.write(self.style.SUCCESS(f"Created {len(categories)} flower categories."))
        return categories

    def _seed_flowers(self, categories):
        if Flower.objects.exists():
            self.stdout.write("Flowers already exist — skipping.")
            return

        by_name = {c.name: c for c in categories}

        flowers_data = [
            ("Crimson Rose Bouquet", "Roses", 3500, "A dozen deep red roses, hand-tied with eucalyptus.", True, True),
            ("Blush Garden Rose Bunch", "Roses", 2800, "Soft pink garden roses with delicate petals.", True, True),
            ("White Rose Elegance", "Roses", 3200, "Pure white roses for timeless occasions.", True, False),
            ("Sunset Mixed Bouquet", "Bouquets", 4200, "A vibrant mix of seasonal flowers in warm tones.", True, True),
            ("Wildflower Meadow Bunch", "Bouquets", 2600, "Loose, natural wildflowers with a rustic charm.", True, False),
            ("Pastel Dream Bouquet", "Bouquets", 3100, "Soft pastel blooms arranged with baby's breath.", True, False),
            ("Bridal Cascade Bouquet", "Wedding Flowers", 8500, "A cascading bouquet of roses, peonies, and greenery.", True, True),
            ("Bridesmaid Posy", "Wedding Flowers", 3800, "A coordinating smaller bouquet for bridesmaids.", True, False),
            ("Wedding Arch Florals", "Wedding Flowers", 15000, "Lush floral arrangement for wedding arches.", True, False),
            ("Balloon & Bloom Birthday Bunch", "Birthday Flowers", 3400, "Bright gerberas and sunflowers for a birthday surprise.", True, True),
            ("Golden Celebration Bouquet", "Birthday Flowers", 3600, "Yellow and orange blooms to celebrate in style.", True, False),
            ("Forever Love Anniversary Roses", "Anniversary Flowers", 4500, "Long-stem roses arranged for a milestone anniversary.", True, True),
            ("Golden Years Bouquet", "Anniversary Flowers", 4000, "A refined bouquet in gold and cream tones.", True, False),
            ("Congratulations Grad Bouquet", "Graduation Flowers", 2900, "A cheerful bouquet to celebrate academic success.", True, False),
            ("Bright Future Sunflower Bunch", "Graduation Flowers", 2700, "Sunflowers symbolizing bright futures ahead.", False, False),
            ("Corporate Elegance Centerpiece", "Event Flowers", 6500, "A statement centerpiece for corporate events.", True, False),
            ("Gala Night Arrangement", "Event Flowers", 7200, "Dramatic florals for evening events and galas.", True, False),
            ("Thank You Gift Bunch", "Gift Flowers", 2400, "A simple, thoughtful bunch to say thank you.", True, False),
            ("Get Well Soon Posy", "Gift Flowers", 2200, "Gentle, cheerful blooms to brighten someone's day.", True, False),
            ("New Baby Bouquet", "Gift Flowers", 3000, "Soft pastel flowers to welcome a new arrival.", False, False),
        ]

        created = 0
        for name, cat_name, price, desc, available, featured in flowers_data:
            flower = Flower.objects.create(
                name=name,
                category=by_name.get(cat_name),
                description=(
                    f"{desc} Hand-arranged by our florists using the freshest "
                    "seasonal stems, finished with premium wrapping and a "
                    "personal touch. Perfect for gifting or displaying at home."
                ),
                short_description=desc,
                price=price,
                available=available,
                featured=featured,
            )
            flower.main_image.save(
                f"{flower.slug}.jpg",
                make_placeholder_image(name, seed=name),
                save=True,
            )
            # Add one or two extra gallery images for a handful of flowers.
            if created % 3 == 0:
                extra = FlowerImage(flower=flower, caption=f"{name} — close-up", order=1)
                extra.image.save(
                    f"{flower.slug}-extra.jpg",
                    make_placeholder_image(f"{name} 2", seed=f"{name}-2"),
                    save=True,
                )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} flowers."))

    def _seed_events(self):
        if Event.objects.exists():
            self.stdout.write("Events already exist — skipping.")
            return

        today = timezone.localdate()

        upcoming = [
            ("Summer Wedding 2026", "Weddings", 25, "Karen Country Club, Nairobi", "A romantic garden wedding styled entirely by Miracle Flowers."),
            ("Corporate Gala Evening", "Corporate events", 40, "Radisson Blu, Nairobi", "An elegant evening gala with statement floral centerpieces."),
            ("Graduation Celebration Pop-Up", "Graduation ceremonies", 55, "University of Nairobi Grounds", "A festive flower stand for graduating students and families."),
        ]
        completed = [
            ("Spring Floral Exhibition", "Floral exhibitions", -30, "Nairobi Arboretum", "Our seasonal showcase of floral design and arrangement techniques."),
            ("Golden Anniversary Celebration", "Anniversaries", -60, "Villa Rosa Kempinski, Nairobi", "A golden-themed floral celebration for a 50th wedding anniversary."),
            ("Charity Ball Centerpieces", "Special celebrations", -90, "Sarova Stanley, Nairobi", "Elegant centerpieces created for an annual charity fundraising ball."),
            ("Birthday in Bloom", "Birthday celebrations", -15, "Private Residence, Karen", "A birthday party transformed with an abundance of fresh flowers."),
        ]

        created = 0
        for title, occasion, offset_days, location, desc in upcoming:
            event = Event.objects.create(
                title=title,
                short_description=desc,
                description=(
                    f"{desc} Join us as Miracle Flowers brings this "
                    f"{occasion.lower()} to life with fresh, hand-arranged "
                    "florals designed for the occasion."
                ),
                event_date=today + datetime.timedelta(days=offset_days),
                event_time=datetime.time(17, 0),
                location=location,
                status=Event.Status.UPCOMING,
            )
            event.featured_image.save(
                f"{event.slug}.jpg",
                make_placeholder_image(title, seed=title),
                save=True,
            )
            created += 1

        for title, occasion, offset_days, location, desc in completed:
            event = Event.objects.create(
                title=title,
                short_description=desc,
                description=(
                    f"{desc} This {occasion.lower()} was one of our favorite "
                    "recent projects, showcasing seasonal blooms and "
                    "custom floral design."
                ),
                event_date=today + datetime.timedelta(days=offset_days),
                event_time=datetime.time(18, 30),
                location=location,
                status=Event.Status.COMPLETED,
            )
            event.featured_image.save(
                f"{event.slug}.jpg",
                make_placeholder_image(title, seed=title),
                save=True,
            )
            # Add a couple of gallery photos per completed event.
            for i in range(1, 3):
                photo = EventPhoto(event=event, caption=f"{title} — moment {i}")
                photo.image.save(
                    f"{event.slug}-photo-{i}.jpg",
                    make_placeholder_image(f"{title} {i}", seed=f"{title}-{i}"),
                    save=True,
                )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} events with photos."))
