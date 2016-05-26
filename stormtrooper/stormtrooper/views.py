from django.http.response import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('task-list'))
    else:
        raise Http404()
