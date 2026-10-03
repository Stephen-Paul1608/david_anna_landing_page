from django.core.management.base import BaseCommand
from django.utils.text import slugify
from ministry.models import Event


class Command(BaseCommand):
    help = "Clean up event slugs to remove invalid URL characters (like &)"

    def handle(self, *args, **options):
        events = Event.objects.all()
        cleaned = 0

        for event in events:
            original_slug = event.slug
            cleaned_slug = slugify(event.slug)

            if original_slug != cleaned_slug:
                event.slug = cleaned_slug
                event.save(update_fields=["slug"])
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Cleaned '{original_slug}' → '{cleaned_slug}' for event: {event.title}"
                    )
                )
                cleaned += 1

        self.stdout.write(
            self.style.SUCCESS(f"\n✓ Done! Cleaned {cleaned} event slug(s).")
        )
