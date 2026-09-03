from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class FlowerCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Flower Category"
        verbose_name_plural = "Flower Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("flowers:catalog") + f"?category={self.slug}"


class Flower(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    category = models.ForeignKey(
        FlowerCategory,
        related_name="flowers",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    description = models.TextField(
        help_text="Full description shown on the flower detail page."
    )
    short_description = models.CharField(
        max_length=200,
        help_text="Short summary shown on catalog and featured cards.",
    )
    price = models.DecimalField(max_digits=9, decimal_places=2)
    main_image = models.ImageField(upload_to="flowers/")
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Flower"
        verbose_name_plural = "Flowers"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Flower.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("flowers:detail", kwargs={"slug": self.slug})

    @property
    def related_flowers(self):
        qs = Flower.objects.filter(available=True)
        if self.category_id:
            qs = qs.filter(category_id=self.category_id)
        return qs.exclude(pk=self.pk)[:4]


class FlowerImage(models.Model):
    flower = models.ForeignKey(Flower, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="flowers/gallery/")
    caption = models.CharField(max_length=150, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Flower Image"
        verbose_name_plural = "Flower Images"

    def __str__(self):
        return f"Image for {self.flower.name}"
