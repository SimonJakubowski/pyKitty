from kitty.models import Kitty, KittyUser, UserItem
from django.http import HttpResponse
from django.core import serializers
from django.utils import simplejson
from django.forms.models import model_to_dict
from kitty import ajax

def kitty(request, id):
    k = Kitty.objects.get(id=id)
    k_json = {
        "kittyId": k.id,
        "name": k.name,
        "createdBy": k.created_by
    }
    return HttpResponse(simplejson.dumps(k_json), content_type="application/json")

def users(request, id):
    k = Kitty.objects.get(id=id)
    u = KittyUser.objects.filter(kitty=k)

    u_json = []
    for user in u:
        u_json.append(dict(userId = user.id, name = user.name, money = user.money))

    return HttpResponse(simplejson.dumps(u_json), content_type="application/json")

def userItems(request, user_id):
    user = KittyUser.objects.get(id=user_id)

    i_json = []
    for useritem in user.useritem_set.all():
        i_json.append(dict(itemId = useritem.id, itemName = useritem.item.name, itemPrice = useritem.item.price, itemEAN = useritem.item.EAN, itemCount = useritem.quantity))

    return HttpResponse(simplejson.dumps(i_json), content_type="application/json")

def incItem(request, user_item_id):
    ajax.incItem(request, user_item_id)
    useritem = UserItem.objects.get(id = user_item_id)
    i_json = dict(itemId = useritem.id, itemName = useritem.item.name, itemPrice = useritem.item.price, itemCount = useritem.quantity, userMoney=useritem.user.money)
    return HttpResponse(simplejson.dumps(i_json), content_type="application/json")

def decItem(request, user_item_id):
    ajax.decItem(request, user_item_id)
    useritem = UserItem.objects.get(id = user_item_id)
    i_json = dict(itemId = useritem.id, itemName = useritem.item.name, itemPrice = useritem.item.price, itemCount = useritem.quantity, userMoney=useritem.user.money)
    return HttpResponse(simplejson.dumps(i_json), content_type="application/json")