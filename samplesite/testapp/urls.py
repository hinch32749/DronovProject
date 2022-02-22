from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import index_test, add_img, get_img, delete_img, add_several_img

namespace = 'testapp'

urlpatterns = [
    path('index/', index_test, name='index_test'),
    path('add_img/', add_img, name='add_img'),
    path('add_several_img/', add_several_img, name='add_several_img'),
    path('get_img/<int:pk>/', get_img, name='get_img'),
    path('delete_img/<int:pk>/', delete_img, name='delete_img'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)