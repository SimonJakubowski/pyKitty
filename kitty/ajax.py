from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from dajax.core import Dajax
from kitty.models import ItemForm, KittyUser, KittyUserForm, Item, UserItem
from django.db.models import Sum
import redis
from django.http import HttpResponseServerError
from django.utils import simplejson
from django.core import serializers

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
        brodcastNewItem(item)
    else:
        dajax.remove_css_class('.form-group', 'has-error')
        for error in item_form.errors:
            dajax.script("$('#id_%s').parent().parent().addClass('has-error')" % error)
   
    return dajax.json()

def brodcastNewItem(item):
    try:
        # brodcast via redis to node.js Server
        r = redis.StrictRedis(host='localhost', port=6379, db=0)

        user_items = serializers.serialize("json", item.useritem_set.all())
        message = {
            "action": "new_item",
            "item_name": item.name,
            "item_price": item.price,
            "item_id": item.id,
            "item_quantity": item.quantity,
            "user_items": user_items,
        }
        
        r.publish(item.kitty_id, simplejson.dumps(message))

    except Exception, e:
        return HttpResponseServerError(str(e))

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
        brodcastNewUser(user)
    else:
        dajax.remove_css_class('.form-group', 'has-error')
        for error in user_form.errors:
            dajax.script("$('#id_%s').parent().parent().addClass('has-error')" % error)

    return dajax.json()

def brodcastNewUser(user):
    try:
        # brodcast via redis to node.js Server
        r = redis.StrictRedis(host='localhost', port=6379, db=0)

        user_items = serializers.serialize("json", user.useritem_set.all())
        message = {
            "action": "new_user",
            "id":user.id,
            "name":user.name,
            "money":user.money,
            "user_items":user_items,
        }

        r.publish(user.kitty_id, simplejson.dumps(message))

    except Exception, e:
        return HttpResponseServerError(str(e))

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
    dajax.assign('#id_item_quantity_consumed_%s'%item.id, 'innerHTML', item_quantity['quantity__sum'])
    dajax.assign('#id_item_quantity_available_%s'%item.id, 'innerHTML', item.quantity - item_quantity['quantity__sum'])

    brodcastUpdateUserItem(user_item)

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
    dajax.assign('#id_item_quantity_consumed_%s'%item.id, 'innerHTML', item_quantity['quantity__sum'])
    dajax.assign('#id_item_quantity_available_%s'%item.id, 'innerHTML', item.quantity - item_quantity['quantity__sum'])

    brodcastUpdateUserItem(user_item)

    return dajax.json()

def brodcastUpdateUserItem(user_item):
    try:
        # brodcast via redis to node.js Server
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        item = user_item.item
        item_quantity = item.useritem_set.all().aggregate(Sum('quantity'))
        message = {
            "action": "update_user_item",
            "user_item_id": user_item.id,
            "user_item_quantity" : user_item.quantity,
            "user_id" : user_item.user.id,
            "user_name" : user_item.user.name,
            "user_money" : user_item.user.money,
            "item_id": user_item.item.id,
            "item_quantity": item.quantity,
            "item_quantity_sum": item_quantity['quantity__sum'],
        }
        
        r.publish(user_item.user.kitty.id, simplejson.dumps(message))

    except Exception, e:
        return HttpResponseServerError(str(e))

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

@dajaxice_register
def editUser(request, form, user_id):
    dajax = Dajax()
    form = deserialize_form(form)
    user = KittyUser.objects.get(id = user_id)
    user_form = KittyUserForm(form, instance=user)

    if user_form.is_valid():
        dajax.remove_css_class('.form-group', 'has-error')
        # create new item in DB
        user = user_form.save()

        dajax.script("$('#editUserModal').modal('hide');")
        dajax.script("location.reload();")
    else:
        dajax.remove_css_class('.form-group', 'has-error')
        for error in user_form.errors:
            dajax.script("$('#id_%s').parent().parent().addClass('has-error')" % error)
   
    return dajax.json()