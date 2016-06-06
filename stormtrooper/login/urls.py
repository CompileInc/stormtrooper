from django.conf.urls import url
from django.views.generic import TemplateView


urlpatterns = (url(r'^login/$', TemplateView.as_view(template_name='login/login.html'), name="accounts-login"),)
