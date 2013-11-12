from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from dajax.core import Dajax
from kitty.models import ItemForm, KittyUser, KittyUserForm, Item, UserItem
from django.db.models import Sum

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

@dajaxice_register
def addUser(request, form):
    dajax = Dajax()
    form = deserialize_form(form)
    k_id = form['kitty_id']
    user_form = KittyUserForm(form)

    if user_form.is_valid():
        dajax.remove_css_class('.form-group', 'has-error')
        user = user_form.save(commit=False)
        user.kitty_id = k_id
        user.save()
         # create item <-> User Connection
        for item in Item.objects.filter(kitty_id = k_id):
            if not user.useritem_set.filter(item=item).exists():
                UserItem.objects.create(item=item, quantity=0, user=user)
        dajax.script("$('#newUserModal').modal('hide');")
        dajax.script("location.reload();")
    else:
        dajax.remove_css_class('.form-group', 'has-error')
        for error in user_form.errors:
            dajax.script("$('#id_%s').parent().parent().addClass('has-error')" % error)

    return dajax.json()

@dajaxice_register
def incItem(request, item_id):
    dajax = Dajax()
    
    user_item = UserItem.objects.get(id = item_id)

    # inc item count
    user_item.quantity += 1
        
    # dec money of user
    user = user_item.user;
    user.money -= user_item.item.price;
    
    # save both
    user_item.save()
    user.save()

    item = user_item.item
    item_quantity = item.useritem_set.all().aggregate(Sum('quantity'))

    # change frontend to new value
    dajax.assign('#id_user_item_%s'%item_id, 'innerHTML', user_item.quantity)
    dajax.assign('#id_user_name_%s'%user.id, 'innerHTML', '%s (%s EUR)'% (user.name, user.money))
    dajax.assign('#id_item_quantity_%s'%item.id, 'innerHTML', item_quantity['quantity__sum'])
    dajax.assign('#id_item_quantity_left_%s'%item.id, 'innerHTML', item.quantity - item_quantity['quantity__sum'])

    return dajax.json()

@dajaxice_register
def decItem(request, item_id):
    dajax = Dajax()
    
    user_item = UserItem.objects.get(id = item_id)
    
    # dec item count
    user_item.quantity -= 1
        
    # giv back money to user
    user = user_item.user;
    user.money += user_item.item.price;
    
    # save both
    user_item.save()
    user.save()

    item = user_item.item
    item_quantity = item.useritem_set.all().aggregate(Sum('quantity'))

    # change frontend to new value
    dajax.assign('#id_user_item_%s'%item_id, 'innerHTML', user_item.quantity)
    dajax.assign('#id_user_name_%s'%user.id, 'innerHTML', '%s (%s EUR)'% (user.name, user.money))
    dajax.assign('#id_item_quantity_%s'%item.id, 'innerHTML', item_quantity['quantity__sum'])
    dajax.assign('#id_item_quantity_left_%s'%item.id, 'innerHTML', item.quantity - item_quantity['quantity__sum'])

    return dajax.json()

@dajaxice_register
def editItem(request, form, item_id):
    dajax = Dajax()
    form = deserialize_form(form)
    item = Item.objects.get(id = item_id)
    item_form = ItemForm(form, instance=item)

    if item_form.is_valid():
        dajax.remove_css_class('.form-group', 'has-error')
        # create new item in DB
        item = item_form.save()

        dajax.script("$('#editItemModal').modal('hide');")
        dajax.script("location.reload();")
    else:
        dajax.remove_css_class('.form-group', 'has-error')
        for error in item_form.errors:
            dajax.script("$('#id_%s').parent().parent().addClass('has-error')" % error)
   
    return dajax.json()