from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from login.models import Trooper


class LoginView(TemplateView):
    template_name = "login/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home'))
        return super(LoginView, self).dispatch(request, *args, **kwargs)


class TrooperView(DetailView):
    slug_field = 'username'
    slug_url_kwarg = 'username'
    model = Trooper
