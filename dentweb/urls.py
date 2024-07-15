from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView



urlpatterns = [
    path('admin/', admin.site.urls),
		path('', include('main.urls')),
		# path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
		# path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
