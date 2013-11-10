from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Welcome Page:
    url(r'^$', 'kitty.views.home', name='home'),
    # creating a kitty
    url(r'^create/', 'kitty.views.create', name='create'),
    # for setting language
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # url(r'^kitty/', include('kitty.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)