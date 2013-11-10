from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from dajax.core import Dajax
from kitty.models import ItemForm, KittyUser

@dajaxice_register
def addItem(request, form):
    dajax = Dajax()
    form = deserialize_form(form)
    k_id = form['kitty_id']
    item_form = ItemForm(form)

    if item_form.is_valid():
        dajax.remove_css_class('.form-group', 'has-error')
        # create new item in DB
        item = item_form.save(commit=False)
        item.kitty_id = k_id
        item.save()
        # create item <-> User Connection
        for user in KittyUser.objects.filter(kitty_id = k_id):
            if not user.useritem_set.filter(item=item).exists():
                UserItem.objects.create(item=item, quantity=0, user=user)
        dajax.script("$('#newItemModal').modal('hide');")
        dajax.script("location.reload();")
    else:
        dajax.remove_css_class('.form-group', 'has-error')
        for error in item_form.errors:
            dajax.script("$('#id_%s').parent().parent().addClass('has-error')" % error)
   
    return dajax.json()