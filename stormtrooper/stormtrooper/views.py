from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('task-list'))
    else:
        return render(request, 'stormtrooper/homepage.html')
