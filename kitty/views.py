from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.utils import translation
from kitty.models import KittyForm, Kitty, Item, KittyUser
from django.db.models import Sum

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

def show(request, id):
    k = Kitty.objects.get(id=id) # requested kitty
    i = Item.objects.filter(kitty=k).annotate(Sum('useritem__quantity')) # items
    u = KittyUser.objects.filter(kitty=k) # kitty user

    return render(request, 'show.html', {  'LANGUAGES':LANGUAGES,
                                            'title': k.name, 
                                            'k':k, 
                                            'i':i, 
                                            'u':u,})