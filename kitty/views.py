from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.utils import translation
from kitty.models import KittyForm

LANGUAGES = (
  ('de', _('German')),
  ('en', _('English')),
)

def home(request):
    return render(request, 'welcome_page.html', {'LANGUAGES':LANGUAGES,})

def create(request):
    if request.method == 'POST':
        form = KittyForm(request.POST)
        if form.is_valid():
            newKitty = form.save()
            return HttpResponseRedirect('../%s' % newKitty.id)
    else:
        form = KittyForm()
    return render(request, 'create.html', {'LANGUAGES':LANGUAGES, 'form':form,})