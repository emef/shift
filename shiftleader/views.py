from pprint import pprint

from django.http import Http404
from django.shortcuts import get_object_or_404
from shift.jobs.models import Job, Shift
from shift import render_page, admin_required, choice_rassoc

import shift_settings as settings

# constants
from shift.jobs.models import JOB_OPEN, JOB_STATUS_CHOICES

@admin_required('shiftleader')
def control_panel(request):
    return render_page(request, 'shiftleader/control_panel.html')

@admin_required('shiftleader')
def open_jobs_list(request):
    open_id = choice_rassoc(JOB_OPEN, JOB_STATUS_CHOICES)
    qs = Job.objects.select_related().filter(status=open_id)
    jobs = []
    for j in qs.all():
        shifts = j.open_shifts()
        if len(shifts):
            jobs.append( { 'job': j, 'shifts': shifts } )
    
    return render_page(request, 'shiftleader/open_jobs_list.html', {'jobs': jobs})

@admin_required('shiftleader')
def open_jobs_calendar(request):
    return render_page(request, 'shiftleader/open_jobs_calendar.html')

@admin_required('shiftleader')
def open_jobs_gantt(request):
    return render_page(request, 'shiftleader/open_jobs_gantt.html')

@admin_required('shiftleader')
def open_jobs_job(request, job_id):
    try:
        job = Job.objects.select_related().get(id=job_id)
    except Job.DoesNotExist:
        raise Http404
    return render_page(request, 'shiftleader/open_jobs_job.html', {'job': job})

@admin_required('shiftleader')
def open_jobs_shift(request, shift_id):
    shift = get_object_or_404(Shift, id=shift_id)
    candidates = shift.candidates(settings.MAX_CANDIDATES)
    data = { 'shift': shift, 'candidates': candidates }
    return render_page(request, 'shiftleader/open_jobs_shift.html', data)

@admin_required('shiftleader')
def contractors_search(request, query):
    return render_page(request, 'shiftleader/contractors_search.html')

@admin_required('shiftleader')
def contractors_detail(request, contractor_id):
    return render_page(request, 'shiftleader/contractors_detail.html')

@admin_required('shiftleader')
def unassigned_jobs(request):
    return render_page(request, 'shiftleader/unassigned_jobs.html')

@admin_required('shiftleader')
def unassigned_detail(request, job_id):
    return render_page(request, 'shiftleader/unassigned_detail.html')

@admin_required('shiftleader')
def unassigned_assign(request, shift_id):
    return render_page(request, 'shiftleader/unassigned_assign.html')

@admin_required('shiftleader')
def completed_jobs(request):
    return render_page(request, 'shiftleader/completed_jobs.html')

@admin_required('shiftleader')
def completed_detail(request, job_id):
    return render_page(request, 'shiftleader/completed_detail.html')


control_panel.title = 'Shift Leader Control Panel'
control_panel.section = 'shiftleader'

open_jobs_list.title = 'Open Jobs (List View)'
open_jobs_list.section = 'shiftleader'
open_jobs_list.page = 'openjobs_list'

open_jobs_calendar.title = 'Open Jobs (Calendar View)'
open_jobs_calendar.section = 'shiftleader'
open_jobs_calendar.page = 'openjobs_calendar'

open_jobs_gantt.title = 'Open Jobs (Gantt Chart)'
open_jobs_gantt.section = 'shiftleader'
open_jobs_gantt.page = 'openjobs_gantt'

open_jobs_job.title = 'Open Job Detail'
open_jobs_job.section = 'shiftleader'

open_jobs_shift.title = 'Open Shift Detail'
open_jobs_shift.section = 'shiftleader'

contractors_search.title = 'Search Contractors'
contractors_search.section = 'shiftleader'
contractors_search.page = 'contractors_search'

contractors_detail.title = 'Contractor Detail'
contractors_detail.section = 'shiftleader'

unassigned_jobs.title = 'Unassigned Jobs'
unassigned_jobs.section = 'shiftleader'
unassigned_jobs.page = 'unassigned_jobs'

unassigned_detail.title = 'Unassigned Job Detail'
unassigned_detail.section = 'shiftleader'

unassigned_assign.title = 'Assign a Shift'
unassigned_assign.section = 'shiftleader'

completed_jobs.title = 'Completed Jobs List'
completed_jobs.section = 'shiftleader'
completed_jobs.page = 'completed_jobs'

completed_detail.title = 'Completed Job Detail'
completed_detail.section = 'shiftleader'

