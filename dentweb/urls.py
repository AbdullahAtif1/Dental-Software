from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns


urlpatterns = i18n_patterns(
    path('bckend-admin/', admin.site.urls),
		path('', include('main.urls')),
		path('<str:name>/blog/', include('blog.urls')),
		path('cstm-admin-panel/', include('dentadmin.urls')),

		path('tinymce/', include('tinymce.urls')),

		# path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
		# path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)