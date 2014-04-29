from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import ninjadev.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ninjadin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^ninjadev$', ninjadev.views.NamespaceView.create,
        name="namespaces-base",),
    url(r'^ninjadev/search$', ninjadev.views.NamespaceView.search_read,
        name="namespaces-search",),
    url(r'^ninjadev/([\w-]+)/choice$', ninjadev.views.choice_POST_handler),
    url(r'^ninjadev/([\w-]+)/([\w-]+)$', ninjadev.views.table_POST_handler),
    url(r'^ninjadev/([\w-]+)/$', ninjadev.views.NamespaceView.update_delete),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()