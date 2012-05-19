from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('shift.clientmanager.views',
    url(r'^$', 'control_panel'),
    url(r'^job/new/$', 'job_new'),
    url(r'^job/open/$', 'job_open'),
    url(r'^job/edit/(?P<job_id>\d+)/$', 'job_edit'),
    url(r'^job/ajax_edit/(?P<job_id>\d+)/$', 'ajax_job_edit'),
    url(r'^job/status/(?P<job_id>\d+)/$', 'job_status'),         
)
