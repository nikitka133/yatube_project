from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from yatube import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls", namespace="users")),
    path("auth/", include("django.contrib.auth.urls")),
    path("", include("posts.urls", namespace="posts")),
    path("about/", include("about.urls", namespace="about")),
]

handler404 = "core.views.page_not_found"
handler500 = "core.views.server_error"
handler403 = "core.views.permission_denied"
CSRF_FAILURE_VIEW = "core.views.csrf_failure"

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
