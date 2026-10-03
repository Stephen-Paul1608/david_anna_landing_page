from django.test import TestCase
from django.urls import reverse

from .models import Testimony


class TestimonyFlowTests(TestCase):
    def test_submission_is_unpublished_by_default(self):
        response = self.client.post(
            reverse("ministry:testimonies"),
            {
                "name": "Sample Name",
                "location": "Bangalore, India",
                "title": "God restored my family",
                "story": "A long story of healing and grace.",
                "category": "family",
                "consent_given": "on",
            },
        )

        self.assertEqual(response.status_code, 302)
        testimony = Testimony.objects.get(name="Sample Name")
        self.assertFalse(testimony.is_published)

    def test_only_published_testimonies_are_listed(self):
        Testimony.objects.create(
            name="Visible",
            location="India",
            title="Visible testimony",
            story="Published story",
            category="salvation",
            is_published=True,
            is_approved=True,
            consent_given=True,
        )
        Testimony.objects.create(
            name="Hidden",
            location="Pakistan",
            title="Hidden testimony",
            story="Draft story",
            category="healing",
            is_published=False,
            is_approved=True,
            consent_given=True,
        )

        response = self.client.get(reverse("ministry:testimonies"))

        self.assertEqual(response.status_code, 200)
        names = [item.name for item in response.context["testimonies"]]
        self.assertEqual(names, ["Visible"])

    def test_legacy_routes_redirect(self):
        response = self.client.get("/invite/", follow=False)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "/contact/")

        response = self.client.get("/blog/", follow=False)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "/testimonies/")

        response = self.client.get("/ministry/", follow=False)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "/#vision")
