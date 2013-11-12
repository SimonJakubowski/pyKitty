from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.utils import translation
from kitty.models import KittyForm, Kitty, Item, ItemForm, KittyUser, KittyUserForm
from django.db.models import Sum
from django.conf import settings

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
    i_form = ItemForm()
    u_form = KittyUserForm()
    return render(request, 'show.html', {  'LANGUAGES':LANGUAGES,
                                            'title': k.name, 
                                            'k':k, 
                                            'i':i, 
                                            'i_form':i_form,
                                            'u':u,
                                            'u_form':u_form,
                                            's_io_server': settings.SOCKET_IO_SERVER,
                                            's_io_port': settings.SOCKET_IO_PORT,})

def itemModal(request, id, itemID):
    item = Item.objects.filter(kitty_id=id).get(id=itemID)
    form = ItemForm(instance=item)

    return render(request, 'modal_view.html', {'identifier':"editItem",
                                               'title':_("edit item"), 
                                               'form':form,
                                               'k_id':id,
                                               'onSave':"editItem(%s);"%itemID})

def userModal(request, id, userID):
    user = KittyUser.objects.filter(kitty_id=id).get(id=userID)
    form = KittyUserForm(instance=user)

    return render(request, 'modal_view.html', {'identifier':"editUser",
                                               'title':_("edit user"), 
                                               'form':form,
                                               'k_id':id,
                                               'onSave':"editUser(%s);"%userID})