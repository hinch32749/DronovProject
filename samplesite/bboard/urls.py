from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from .views import index, BbByRubricView, BbCreateView, BbDetailView

# app_name = 'bboard'

urlpatterns = [
    re_path('^detail/(?P<pk>[0-9]*)/$', BbDetailView.as_view(), name='detail'),
    re_path(r'^add/$', BbCreateView.as_view(), name='add'),
    re_path(r'^(?P<rubric_id>[0-9]*)/$', BbByRubricView.as_view(), name='by_rubric'),
    re_path(r'^$', index, name='index')
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
