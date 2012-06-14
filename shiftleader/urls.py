from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('shift.shiftleader.views',
    url(r'^$', 'control_panel'),
    url(r'open-jobs/$', 'open_jobs_list'),
    url(r'open-jobs/calendar/$', 'open_jobs_calendar'),
    url(r'open-jobs/gantt/$', 'open_jobs_gantt'),
    url(r'open-jobs/job/(?P<job_id>\d+)/$', 'open_jobs_job'),
    url(r'open-jobs/shift/(?P<shift_id>\d+)/$', 'open_jobs_shift'),
    url(r'contractors/search/(?P<query>.*)', 'contractors_search'),
    url(r'contractors/detail/(?P<contractor_id>\d+)/$', 'contractors_detail'),
    url(r'pending-jobs/$', 'pending_jobs'),
    url(r'pending-jobs/job/(?P<job_id>\d+)/$', 'pending_jobs_job'),
    url(r'pending-jobs/shift/(?P<shift_id>\d+)/$', 'pending_jobs_shift'),
    url(r'completed-jobs/$', 'completed_jobs'),
    url(r'completed-jobs/detail/(?P<job_id>\d+)/$', 'completed_detail'),
)
