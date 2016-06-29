from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.context import RequestContext


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('task-list'))
    else:
        return render_to_response('stormtrooper/homepage.html', RequestContext(request, {}))
