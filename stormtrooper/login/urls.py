from django.conf.urls import url, include
from login.views import LoginView
from django.contrib.auth.views import logout


urlpatterns = (url(r'^login/$', LoginView.as_view(), name="accounts-login"),
               url(r'^logout/$', logout, {'template_name': 'login/logout.html'}, name="accounts-logout"),
               url('', include('social.apps.django_app.urls', namespace='social')),)
