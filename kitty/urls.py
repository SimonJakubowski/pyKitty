from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',
    # Welcome Page:
    url(r'^$', 'kitty.views.home', name='home'),
    # creating a kitty
    url(r'^create/', 'kitty.views.create', name='create'),
    # display item Modal
    url(r'^(?P<id>\w{5})/itemModal/(?P<itemID>\d+)/', 'kitty.views.itemModal'),
    # display user Modal
    url(r'^(?P<id>\w{5})/userModal/(?P<userID>\d+)/', 'kitty.views.userModal'),
    # display kitty with ID
    url(r'^(?P<id>\w{5})/', 'kitty.views.show'),
    # for setting language
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # Dajax
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    
    # url(r'^kitty/', include('kitty.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

# API URLS
urlpatterns += patterns('kitty.api',
    url(r'^api/incItem/(?P<user_item_id>\d+)', 'incItem'),
    url(r'^api/decItem/(?P<user_item_id>\d+)', 'decItem'),
    url(r'^api/userItems/(?P<user_id>\d+)', 'userItems'),
    url(r'^api/users/(?P<id>\w{5})/', 'users'),
    url(r'^api/kitty/(?P<id>\w{5})/', 'kitty'),
)