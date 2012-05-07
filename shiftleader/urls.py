from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('shift.shiftleader.views',
    url(r'^$', 'control_panel'),
    url(r'open-jobs/$', 'open_jobs_list'),
    url(r'open-jobs/calendar/$', 'open_jobs_calendar'),
    url(r'open-jobs/gantt/$', 'open_jobs_gantt'),
    url(r'open-jobs/job-detail/(?P<job_id>\d+)/$', 'open_jobs_job'),
    url(r'open-jobs/shift-detail/(?P<shift_id>\d+)/$', 'open_jobs_shift'),
    url(r'contractors/search/(?P<query>.*)', 'contractors_search'),
    url(r'contractors/detail/(?P<contractor_id>\d+)/$', 'contractors_detail'),
    url(r'unassigned-jobs/$', 'unassigned_jobs'),
    url(r'unassigned-jobs/detail/(?P<job_id>\d+)/$', 'unassigned_detail'),
    url(r'unassigned-jobs/assign/(?P<shift_id>\d+)/$', 'unassigned_assign'),
    url(r'completed-jobs/$', 'completed_jobs'),
    url(r'completed-jobs/detail/(?P<job_id>\d+)/$', 'completed_detail'),                       
)
