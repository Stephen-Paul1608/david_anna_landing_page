from django.urls import path

from . import views

app_name = "ministry"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("messages/", views.messages_list, name="messages"),
    path("messages/<slug:slug>/", views.message_detail, name="message_detail"),
    path("events/", views.events_list, name="events"),
    path("events/<slug:slug>/", views.event_detail, name="event_detail"),
    path("media/", views.media_page, name="media"),
    path("testimonies/", views.testimonies_page, name="testimonies"),
    path("testimonies/<slug:slug>/", views.testimony_detail, name="testimony_detail"),
    path("contact/", views.contact, name="contact"),
    path("todays-word/", views.todays_word, name="todays_word"),
    path("newsletter/", views.newsletter_signup, name="newsletter"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
    path("invite/", views.redirect_invite, name="invite"),
    path("blog/", views.redirect_blog, name="blog"),
    path("blog/<slug:slug>/", views.redirect_blog, name="article_detail"),
    path("ministry/", views.redirect_ministry, name="ministry"),
]
