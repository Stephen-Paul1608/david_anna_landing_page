from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from ministry.views import robots_txt, sitemap

admin.site.site_header = "David Sudher Ministries"
admin.site.site_title = "DSM Admin"
admin.site.index_title = "Content"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, name="sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("", include("ministry.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
