from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class SiteSettings(models.Model):
    ministry_name = models.CharField(max_length=120, default="David Sudher Ministries")
    tagline = models.CharField(
        max_length=200,
        default="Raising a generation to know Christ and make Christ known.",
    )
    youtube_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    other_url = models.URLField(blank=True, help_text="Optional additional platform")
    other_label = models.CharField(max_length=40, blank=True)
    youtube_channel_id = models.CharField(
        max_length=80,
        blank=True,
        help_text="For future dynamic YouTube imports",
    )
    contact_email = models.EmailField(blank=True)
    logo = models.ImageField(
        upload_to="branding/",
        blank=True,
        help_text="Official David Sudher Ministries logo. Do not replace with a generated mark.",
    )

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.ministry_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Scripture(models.Model):
    THEME_CHOICES = [
        ("calling", "Calling"),
        ("purpose", "Purpose"),
        ("faith", "Faith"),
        ("evangelism", "Evangelism"),
        ("discipleship", "Discipleship"),
        ("courage", "Courage"),
        ("generation", "Next Generation"),
        ("witness", "Witness"),
    ]
    verse_text = models.TextField()
    reference = models.CharField(max_length=80)
    theme = models.CharField(max_length=24, choices=THEME_CHOICES, default="faith")
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.reference


class TodaysWord(models.Model):
    date = models.DateField(unique=True, default=timezone.now)
    title = models.CharField(max_length=160, default="Today's Word")
    thought = models.TextField()
    verse_text = models.TextField()
    verse_reference = models.CharField(max_length=80)
    encouragement = models.TextField(blank=True)
    prayer = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Today's Word"
        verbose_name_plural = "Today's Words"

    def __str__(self):
        return f"{self.date} — {self.title}"

    def get_absolute_url(self):
        return reverse("ministry:todays_word")


class Article(models.Model):
    CATEGORY_CHOICES = [
        ("faith", "Faith"),
        ("purpose", "Purpose"),
        ("leadership", "Leadership"),
        ("youth", "Youth"),
        ("discipleship", "Discipleship"),
        ("prayer", "Prayer"),
        ("christian-living", "Christian Living"),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES)
    excerpt = models.TextField(max_length=400)
    body = models.TextField()
    image = models.ImageField(upload_to="articles/", blank=True)
    image_fallback = models.CharField(
        max_length=120,
        blank=True,
        help_text="Filename in static/ministry/images/",
    )
    published_at = models.DateField(default=timezone.now)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        else:
            # Ensure slug is always clean (remove invalid characters)
            self.slug = slugify(self.slug)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("ministry:article_detail", args=[self.slug])

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        if self.image_fallback:
            return f"/static/ministry/images/{self.image_fallback}"
        return "/static/ministry/images/hero-preaching.jpg"


class Message(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    preached_on = models.DateField(default=timezone.now)
    youtube_video_id = models.CharField(
        max_length=32,
        blank=True,
        help_text="YouTube video ID for embed, e.g. dQw4w9WgXcQ",
    )
    thumbnail = models.ImageField(upload_to="messages/", blank=True)
    thumbnail_fallback = models.CharField(max_length=120, blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-preached_on"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        else:
            # Ensure slug is always clean (remove invalid characters)
            self.slug = slugify(self.slug)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("ministry:message_detail", args=[self.slug])

    @property
    def thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        if self.youtube_video_id:
            return f"https://i.ytimg.com/vi/{self.youtube_video_id}/hqdefault.jpg"
        if self.thumbnail_fallback:
            return f"/static/ministry/images/{self.thumbnail_fallback}"
        return "/static/ministry/images/speaking-uturn.jpg"

    @property
    def embed_url(self):
        if self.youtube_video_id:
            return f"https://www.youtube.com/embed/{self.youtube_video_id}"
        return ""


class Event(models.Model):
    TYPE_CHOICES = [
        ("conference", "Conference"),
        ("youth", "Youth Gathering"),
        ("church", "Church Service"),
        ("leadership", "Leadership Event"),
        ("ministry", "Ministry Meeting"),
        ("special", "Special Event"),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    event_type = models.CharField(max_length=24, choices=TYPE_CHOICES)
    starts_at = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    registration_url = models.URLField(blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["starts_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        else:
            # Ensure slug is always clean (remove invalid characters)
            self.slug = slugify(self.slug)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("ministry:event_detail", args=[self.slug])


class Testimony(models.Model):
    CATEGORY_CHOICES = [
        ("salvation", "Salvation"),
        ("healing", "Healing"),
        ("provision", "Provision"),
        ("family", "Family"),
        ("calling", "Calling"),
        ("deliverance", "Deliverance"),
    ]

    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=180, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    story = models.TextField()
    excerpt = models.CharField(max_length=220, blank=True)
    photo = models.ImageField(upload_to="testimonies/", blank=True)
    video_url = models.URLField(blank=True)
    category = models.CharField(max_length=24, choices=CATEGORY_CHOICES, default="salvation")
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    consent_given = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Testimonies"

    def __str__(self):
        return self.title or self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title or self.name)
        else:
            self.slug = slugify(self.slug)
        if not self.excerpt and self.story:
            self.excerpt = self.story[:200].strip()
        super().save(*args, **kwargs)

    @property
    def initials(self):
        parts = [part for part in self.name.split() if part]
        if not parts:
            return "T"
        initials = "".join(part[0].upper() for part in parts[:2])
        return initials[:2] or "T"

    def get_absolute_url(self):
        return reverse("ministry:testimony_detail", args=[self.slug])


class NewsletterSignup(models.Model):
    first_name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class ContactSubmission(models.Model):
    TOPIC_CHOICES = [
        ("general", "General Enquiry"),
        ("speaking", "Speaking Invitation"),
        ("partnership", "Ministry Partnership"),
        ("testimony", "Testimony"),
        ("prayer", "Prayer Request"),
    ]
    topic = models.CharField(max_length=24, choices=TOPIC_CHOICES)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    organization = models.CharField(max_length=160, blank=True)
    event_type = models.CharField(max_length=80, blank=True)
    event_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=160, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_topic_display()} — {self.name}"
