from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import hallazgos.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('admin/hallazgos/bulk_upload/', hallazgos.views.hallazgo_bulk_upload, name='hallazgo_bulk_upload'),
    path('hallazgos/', include(hallazgos.urls)),
    path('taggit_autosuggest/', include('taggit_autosuggest.urls')),


]

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

urlpatterns.append(path('', include('cms.urls')))

# the new django admin sidebar is bad UX in django CMS custom admin views.
admin.site.enable_nav_sidebar = False
