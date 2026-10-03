import re
import unicodedata
from datetime import date, datetime
from types import SimpleNamespace

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ContactForm, NewsletterForm, TestimonyForm
from .messages_data import MESSAGES
from .testimonies_data import CATEGORY_LABELS, TESTIMONIES


def _site_settings():
    return SimpleNamespace(
        ministry_name="David Sudher Ministries",
        tagline="Raising a generation to know Christ and make Christ known.",
        youtube_url="",
        instagram_url="",
        facebook_url="",
        other_url="",
        other_label="",
        logo=None,
        contact_email="",
    )


def _page_context(**kwargs):
    ctx = {
        "site_settings": _site_settings(),
        "nav_newsletter_form": NewsletterForm(),
    }
    ctx.update(kwargs)
    return ctx


def _message_data():
    return [
        SimpleNamespace(
            title="Living with Purpose",
            slug="living-with-purpose",
            description="A message about discovering calling, courage, and identity in Christ.",
            preached_on=date(2026, 9, 18),
            thumbnail_url="/static/ministry/images/speaking-uturn.jpg",
            youtube_video_id="dQw4w9WgXcQ",
            is_featured=True,
            is_published=True,
            get_absolute_url=lambda slug="living-with-purpose": reverse("ministry:message_detail", args=[slug]),
            embed_url="https://www.youtube.com/embed/dQw4w9WgXcQ",
        ),
        SimpleNamespace(
            title="The Courage to Go",
            slug="the-courage-to-go",
            description="A practical message on stepping forward in faith with boldness and obedience.",
            preached_on=date(2026, 8, 28),
            thumbnail_url="/static/ministry/images/prayer-community.jpg",
            youtube_video_id="",
            is_featured=False,
            is_published=True,
            get_absolute_url=lambda slug="the-courage-to-go": reverse("ministry:message_detail", args=[slug]),
            embed_url="",
        ),
        SimpleNamespace(
            title="A Heart That Sees God",
            slug="a-heart-that-sees-god",
            description="A call to spiritual renewal, prayer, and deeper awareness of God's presence.",
            preached_on=date(2026, 7, 14),
            thumbnail_url="/static/ministry/images/hero-preaching.jpg",
            youtube_video_id="",
            is_featured=False,
            is_published=True,
            get_absolute_url=lambda slug="a-heart-that-sees-god": reverse("ministry:message_detail", args=[slug]),
            embed_url="",
        ),
    ]


def _event_data():
    return [
        SimpleNamespace(
            title="Youth Awakening Gathering",
            slug="youth-awakening-gathering",
            event_type="youth",
            starts_at=datetime(2026, 11, 12, 18, 30),
            location="Bangalore, India",
            description="An evening of worship, prayer, and encouragement for young people seeking Jesus.",
            registration_url="",
            is_published=True,
            get_absolute_url=lambda slug="youth-awakening-gathering": reverse("ministry:event_detail", args=[slug]),
            get_event_type_display=lambda: "Youth Gathering",
        ),
        SimpleNamespace(
            title="Prayer and Revival night",
            slug="prayer-and-revival-night",
            event_type="special",
            starts_at=datetime(2026, 12, 3, 19, 0),
            location="Hyderabad, India",
            description="A night of prayer, worship, and preaching centered on revival and awakening.",
            registration_url="",
            is_published=True,
            get_absolute_url=lambda slug="prayer-and-revival-night": reverse("ministry:event_detail", args=[slug]),
            get_event_type_display=lambda: "Special Event",
        ),
    ]




def _scripture_data():
    return SimpleNamespace(
        verse_text="You are the light of the world. Let your light shine before others.",
        reference="Matthew 5:14-16",
    )


def _home_context():
    home_videos = MESSAGES[:3]
    event_items = _event_data()[:2]
    featured_testimony = next((item for item in TESTIMONIES if item.get("featured")), TESTIMONIES[0] if TESTIMONIES else None)
    return {
        "todays_word": None,
        "featured_message": home_videos[0],
        "featured_testimony": featured_testimony,
        "testimonies": TESTIMONIES,
        "home_videos": home_videos,
        "events": event_items,
        "scripture": _scripture_data(),
        "newsletter_form": NewsletterForm(),
    }


def home(request):
    context = _home_context()
    context.update(_page_context())
    return render(request, "ministry/home.html", context)


def about(request):
    return render(
        request,
        "ministry/about.html",
        _page_context(scripture=_scripture_data()),
    )


def messages_list(request):
    videos = [
        {
            **video,
            "title": re.sub(
                r" {2,}",
                " ",
                re.sub(r"[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F]", "", unicodedata.normalize("NFKC", video["title"])).strip(),
            ),
        }
        for video in MESSAGES
    ]
    return render(
        request,
        "ministry/messages.html",
        _page_context(videos=videos),
    )


def message_detail(request, slug):
    item = next((msg for msg in _message_data() if msg.slug == slug), None)
    if item is None:
        return redirect("ministry:messages")
    others = [msg for msg in _message_data() if msg.slug != slug][:3]
    return render(request, "ministry/message_detail.html", _page_context(item=item, others=others))


def testimony_detail(request, slug=None):
    return redirect("ministry:testimonies", permanent=True)


def events_list(request):
    upcoming = _event_data()
    return render(request, "ministry/events.html", _page_context(events=upcoming))


def event_detail(request, slug):
    event = next((item for item in _event_data() if item.slug == slug), None)
    if event is None:
        return redirect("ministry:events")
    return render(request, "ministry/event_detail.html", _page_context(event=event))


def media_page(request):
    qs = _message_data()
    return render(request, "ministry/media.html", _page_context(items=qs))


def testimonies_page(request):
    featured = next((item for item in TESTIMONIES if item.get("featured")), TESTIMONIES[0] if TESTIMONIES else None)
    cards = [item for item in TESTIMONIES if item != featured]
    return render(
        request,
        "ministry/testimonies.html",
        _page_context(
            featured=featured,
            testimonies=cards,
            all_testimonies=TESTIMONIES,
            categories=[(key, label) for key, label in CATEGORY_LABELS.items()],
        ),
    )


def contact(request):
    initial = {}
    topic = request.GET.get("topic")
    if topic in {"general", "speaking", "partnership", "testimony", "prayer"}:
        initial["topic"] = topic
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Your message has been received. We will be in touch.")
            return redirect("ministry:contact")
    else:
        form = ContactForm(initial=initial)
    return render(request, "ministry/contact.html", _page_context(form=form))


def redirect_invite(request):
    return redirect("/contact/", permanent=True)


def redirect_blog(request, slug=None):
    return redirect("/testimonies/", permanent=True)


def redirect_ministry(request):
    return redirect("/#vision", permanent=True)


def todays_word(request):
    return render(
        request,
        "ministry/todays_word.html",
        _page_context(todays_word=None, archive=[]),
    )


def newsletter_signup(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        next_url = request.POST.get("next") or "/"
        if form.is_valid():
            messages.success(request, "Welcome. You are now part of the community.")
        else:
            messages.info(request, "That email is already connected, or please check the form.")
        return redirect(next_url)
    return redirect("ministry:home")


def privacy(request):
    return render(request, "ministry/privacy.html", _page_context())


def terms(request):
    return render(request, "ministry/terms.html", _page_context())


class StaticViewSitemap:
    priority = 0.8
    changefreq = "weekly"

    def __call__(self):
        return self

    def items(self):
        return [
            "ministry:home",
            "ministry:about",
            "ministry:messages",
            "ministry:testimonies",
            "ministry:events",
            "ministry:contact",
            "ministry:todays_word",
            "ministry:media",
            "ministry:privacy",
            "ministry:terms",
        ]

    def location(self, item):
        return reverse(item)


def sitemap(request):
    from django.contrib.sitemaps import Sitemap
    from django.contrib.sitemaps.views import sitemap as sitemaps_view

    class SiteSitemap(Sitemap):
        priority = 0.8
        changefreq = "weekly"

        def items(self):
            return [
                "ministry:home",
                "ministry:about",
                "ministry:messages",
                "ministry:testimonies",
                "ministry:events",
                "ministry:contact",
                "ministry:todays_word",
                "ministry:media",
                "ministry:privacy",
                "ministry:terms",
            ]

        def location(self, item):
            return reverse(item)

    return sitemaps_view(request, {"static": SiteSitemap})


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse("sitemap"))
    return HttpResponse(
        f"User-agent: *\nAllow: /\nSitemap: {sitemap_url}\n",
        content_type="text/plain",
    )
