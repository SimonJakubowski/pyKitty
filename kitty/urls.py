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
    # display kitty with ID
    url(r'^(?P<id>\w{5})/itemModal/(?P<itemID>\d+)/', 'kitty.views.itemModal'),
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