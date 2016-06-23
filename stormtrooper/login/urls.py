from django.conf.urls import url, include
from django.contrib.auth.views import logout

from login.views import LoginView, TrooperView


urlpatterns = (url(r'^login/$', LoginView.as_view(), name="accounts-login"),
               url(r'^logout/$', logout, {'template_name': 'login/logout.html'}, name="accounts-logout"),
               url(r'^u/(?P<username>[(\w)(\W)(\s)]+)/$', TrooperView.as_view(), name="accounts-profile"),
               url('', include('social.apps.django_app.urls', namespace='social')),
               )
