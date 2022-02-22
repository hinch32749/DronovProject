from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path, re_path

from .views import BbByRubricView, BbDetailView, BbEditView, \
    BbDeleteView, index, rubrics, search, BbAddView

namespace = 'bboard'

urlpatterns = [
    re_path(r'^search/$', search, name='search'),
    re_path(r'^rubrics/$', rubrics, name='rubrics'),
    re_path('^detail/(?P<pk>[0-9]*)/$', BbDetailView.as_view(), name='detail'),
    # path('detail/<int:year>/<int:month>/<int:day>/<int:pk>',
    #      BbRedirectView.as_view(), name='old_detail'),
    re_path(r'^add/$', BbAddView.as_view(), name='add'),
    re_path(r'^delete/(?P<pk>[0-9]*)$', BbDeleteView.as_view(), name='delete'),
    re_path(r'^correction/(?P<pk>[0-9]*)$', BbEditView.as_view(), name='correction'),
    re_path(r'^(?P<rubric_id>[0-9]*)/$', BbByRubricView.as_view(), name='by_rubric'),
    re_path(r'^$', index, name='index'),
    re_path(r'^accounts/logout/$', LogoutView.as_view(next_page='index'), name='logout'),
    re_path(r'^accounts/login/$', LoginView.as_view(), name='login'),
    re_path(r'^accounts/password_change/$', PasswordChangeView.as_view(
        template_name='registration/change_password.html'),
            name='password_change'),
    re_path(r'^accounts/password_change/done/$', PasswordChangeDoneView.as_view(
        template_name='registration/password_changed.html'),
            name='password_change_done'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
