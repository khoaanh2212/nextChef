from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render


def raise_gone(request):
    return render(request, '410.html', status=410)

@staff_member_required
def clear_cache(request):
    call_command('clear_cache')
    return HttpResponseRedirect(reverse('admin:index'))
