from randomprimary.random_primary import RandomPrimaryIdModel
from django.db import models
from django import forms

# every Kitty has a Random ID
class Kitty(RandomPrimaryIdModel):
    name = models.CharField(max_length=50)
    created_by = models.CharField(max_length=50)

# Form for creating a Kitty
class KittyForm(forms.ModelForm):

    class Meta:
        model = Kitty
        fields = ['name','created_by']

# every Kitty has Items (e.g. a drink, coffee, snack)
class Item(models.Model):
    kitty = models.ForeignKey(Kitty)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    EAN = models.CharField(max_length=13, null=True, blank=True)
    quantity = models.IntegerField(max_length=5)

# every Kitty has users with money (can be negative)
class KittyUser(models.Model):
    kitty = models.ForeignKey(Kitty)
    name = models.CharField(max_length=50)
    money = models.DecimalField(max_digits=5, decimal_places=2)

# connection between user <-> items
# stores users item consumption as quantity 
class UserItem(models.Model):
    item = models.ForeignKey(Item)
    quantity = models.IntegerField(max_length=5)
    user = models.ForeignKey(KittyUser)