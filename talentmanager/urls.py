from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('shift.talentmanager.views',
    url(r'^$', 'control_panel'),
    url(r'^upload', 'upload'),
)
