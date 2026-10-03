from .forms import NewsletterForm
from .models import SiteSettings


def site(request):
    return {
        "site_settings": SiteSettings.get(),
        "nav_newsletter_form": NewsletterForm(),
    }
