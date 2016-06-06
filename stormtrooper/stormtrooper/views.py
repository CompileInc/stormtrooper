from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('task-list'))
    else:
        return HttpResponseRedirect(reverse('accounts-login'))
