from django.contrib import admin

from .models import (
    Article,
    ContactSubmission,
    Event,
    Message,
    NewsletterSignup,
    Scripture,
    SiteSettings,
    Testimony,
    TodaysWord,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("ministry_name", "tagline", "logo", "contact_email")}),
        (
            "Social & YouTube",
            {
                "fields": (
                    "youtube_url",
                    "youtube_channel_id",
                    "instagram_url",
                    "facebook_url",
                    "other_label",
                    "other_url",
                )
            },
        ),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TodaysWord)
class TodaysWordAdmin(admin.ModelAdmin):
    list_display = ("date", "title", "verse_reference", "is_published")
    list_filter = ("is_published",)
    search_fields = ("title", "thought", "verse_text")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_at", "is_featured", "is_published")
    list_filter = ("category", "is_featured", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "excerpt", "body")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("title", "preached_on", "youtube_video_id", "is_featured", "is_published")
    list_filter = ("is_featured", "is_published")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "event_type", "starts_at", "location", "is_published")
    list_filter = ("event_type", "is_published")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "category", "is_published", "is_featured", "is_approved")
    list_filter = ("category", "is_published", "is_featured", "is_approved")
    search_fields = ("name", "title", "story")
    prepopulated_fields = {"slug": ("title",)}
    actions = ["publish_testimonies"]

    @admin.action(description="Publish selected testimonies")
    def publish_testimonies(self, request, queryset):
        queryset.update(is_published=True, is_approved=True)


@admin.register(Scripture)
class ScriptureAdmin(admin.ModelAdmin):
    list_display = ("reference", "theme", "is_featured", "order")
    list_filter = ("theme", "is_featured")


@admin.register(NewsletterSignup)
class NewsletterSignupAdmin(admin.ModelAdmin):
    list_display = ("first_name", "email", "created_at")
    search_fields = ("first_name", "email")


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "topic", "email", "created_at")
    list_filter = ("topic",)
    readonly_fields = ("created_at",)
