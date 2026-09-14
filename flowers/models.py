from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class FlowerCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    slug = models.SlugField(
        max_length=110,
        unique=True,
        blank=True,
    )
    description = models.TextField(
        blank=True,
    )
    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Flower Category"
        verbose_name_plural = "Flower Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 2

            while FlowerCategory.objects.filter(slug=slug).exclude(
                pk=self.pk
            ).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "flowers:catalog"
        ) + f"?category={self.slug}"


class Flower(models.Model):
    category = models.ForeignKey(
        FlowerCategory,
        on_delete=models.SET_NULL,
        related_name="flowers",
        null=True,
        blank=True,
    )

    name = models.CharField(
        max_length=150,
    )

    slug = models.SlugField(
        max_length=170,
        unique=True,
        blank=True,
    )

    short_description = models.CharField(
        max_length=200,
        help_text="Short description shown on flower cards.",
    )

    description = models.TextField(
        help_text="Full description shown on the flower detail page.",
    )

    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
    )

    main_image = models.ImageField(
        upload_to="flowers/",
    )

    available = models.BooleanField(
        default=True,
    )

    featured = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Flower"
        verbose_name_plural = "Flowers"
        indexes = [
            models.Index(fields=["available"]),
            models.Index(fields=["featured"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 2

            while Flower.objects.filter(slug=slug).exclude(
                pk=self.pk
            ).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "flowers:detail",
            kwargs={"slug": self.slug},
        )

    @property
    def related_flowers(self):
        if not self.category_id:
            return Flower.objects.filter(
                available=True
            ).exclude(
                pk=self.pk
            )[:4]

        return Flower.objects.filter(
            category_id=self.category_id,
            available=True,
        ).exclude(
            pk=self.pk
        )[:4]


class FlowerImage(models.Model):
    flower = models.ForeignKey(
        Flower,
        on_delete=models.CASCADE,
        related_name="gallery_images",
    )

    image = models.ImageField(
        upload_to="flowers/gallery/",
    )

    caption = models.CharField(
        max_length=150,
        blank=True,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Flower Gallery Image"
        verbose_name_plural = "Flower Gallery Images"
        indexes = [
            models.Index(fields=["flower", "order"]),
        ]

    def __str__(self):
        return f"{self.flower.name} - Gallery Image {self.pk}"