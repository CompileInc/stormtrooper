from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from login.models import Trooper


class LoginView(TemplateView):
    template_name = "login/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home'))
        return super(LoginView, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class TrooperView(DetailView):
    slug_field = 'username'
    slug_url_kwarg = 'username'
    model = Trooper
