from django.views.generic import TemplateView
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse


class LoginView(TemplateView):
    template_name = "login/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home'))
        return super(LoginView, self).dispatch(request, *args, **kwargs)
