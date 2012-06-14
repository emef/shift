from pprint import pprint

from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from shift.users.models import Contractor
from shift.jobs.models import Job, Shift, ShiftOffer
from shift.shiftleader.emails import send_confirmation_email
from shift import render_page, admin_required, choice_rassoc, choice_assoc

from shift.jobs.models import JOB_OPEN, JOB_PENDING, JOB_STATUS_CHOICES
from shift.jobs.models import SHIFT_OPEN, SHIFT_PENDING, SHIFT_ASSIGNED, SHIFT_STATUS_CHOICES

import shift.shift_settings as settings

# constants
from shift.jobs.models import JOB_OPEN, JOB_STATUS_CHOICES

@admin_required('shiftleader')
def control_panel(request):
    return render_page(request, 'shiftleader/control_panel.html')

@admin_required('shiftleader')
def open_jobs_list(request):
    open_id = choice_rassoc(JOB_OPEN, JOB_STATUS_CHOICES)
    qs = Job.objects.select_related().all()
    jobs = []
    for j in qs:
        open_shifts = j.open_shifts()
        if len(open_shifts):
            jobs.append({'job': j, 'shifts': open_shifts})
    job_url = '/shift-leader/open-jobs/job/'
    shift_url = '/shift-leader/open-jobs/shift/'
    
    return render_page(request, 'jobs_list.html', locals())


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
    
    if request.method == 'POST':
        try:
            standby = map(int, request.POST.getlist('standby'))
        except KeyError, ValueError:
            raise Http404

        # remove old offers
        shift.offers.all().delete()
        
        for id in standby:
            offer = ShiftOffer(contractor_id=id, shift=shift)
            offer.save()
            #send_confirmation_email(offer)
            
        shift.status = choice_rassoc(SHIFT_PENDING, SHIFT_STATUS_CHOICES)
        shift.save()
        
        if len(shift.job.open_shifts()) == 0:
            shift.job.status = choice_rassoc(JOB_PENDING, JOB_STATUS_CHOICES)
            shift.job.save()

        return redirect('/shift-leader/pending-jobs/shift/%s' % shift.id)
            
    return render_page(request, 'shiftleader/open_jobs_shift.html', data)


@admin_required('shiftleader')
def contractors_search(request, query):
    return render_page(request, 'shiftleader/contractors_search.html')

@admin_required('shiftleader')
def contractors_detail(request, contractor_id):
    return render_page(request, 'shiftleader/contractors_detail.html')

@admin_required('shiftleader')
def pending_jobs(request):
    pending_id = choice_rassoc(JOB_PENDING, JOB_STATUS_CHOICES)
    qs = Job.objects.select_related().all()
    jobs = []
    for j in qs:
        pending_shifts = j.pending_shifts()
        if len(pending_shifts):
            jobs.append({'job': j, 'shifts': pending_shifts})
    job_url = '/shift-leader/pending-jobs/job/'
    shift_url = '/shift-leader/pending-jobs/shift/'
    
    return render_page(request, 'jobs_list.html', locals())

@admin_required('shiftleader')
def pending_jobs_job(request, job_id):
    return render_page(request, 'shiftleader/unassigned_detail.html')

@admin_required('shiftleader')
def pending_jobs_shift(request, shift_id):
    shift = get_object_or_404(Shift, pk=shift_id)
    
    errors = []
    if request.method == 'POST':
        if 'hire' in request.POST:
            try: 
                id = int(request.POST['hire'])
                contractor = Contractor.objects.get(id=id)
                shift.contractor_id = id
                
                if 'standby' in request.POST:
                    standby = map(int, request.POST.getlist('standby'))
                    
                    for sc in Contractor.objects.filter(id__in=standby):
                        shift.standby_contractors.add(sc)
                    
                shift.offers.all().delete()
                contractor.offers.all().delete()
                
                shift.status = choice_rassoc(SHIFT_ASSIGNED, SHIFT_STATUS_CHOICES)
                shift.save()

                if len(shift.job.pending_shifts()) == 0:
                    shift.job.status = choice_rassoc(JOB_ASSIGNED, JOB_STATUS_CHOICES)
                    shift.job.save()

                return redirect('/shift-leader/pending-jobs/')
                
                    
            except ValueError:
                errors.append('You must select a contractor')
            
    
    confirmed = []
    unknown = []
    for offer in shift.offers.all():
        if offer.confirmed == True:
            confirmed.append(offer.contractor)
        elif offer.confirmed == None:
            unknown.append(offer.contractor)
    return render_page(request, 'shiftleader/pending_jobs_shift.html', locals())

@admin_required('shiftleader')
def completed_jobs(request):
    return render_page(request, 'shiftleader/completed_jobs.html')

@admin_required('shiftleader')
def completed_detail(request, job_id):
    return render_page(request, 'shiftleader/completed_detail.html')


def confirm_shift(request, uid):
    offer = get_object_or_404(ShiftOffer, uid=uid)
    offer.confirmed = True
    offer.save()
    return render_page(request, 'confirmation.html')

def unconfirm_shift(request, uid):
    offer = get_object_or_404(ShiftOffer, uid=uid)
    offer.confirmed = False
    offer.save()
    return render_page(request, 'confirmation.html')    


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

pending_jobs.title = 'Pending Jobs'
pending_jobs.section = 'shiftleader'
pending_jobs.page = 'pending_jobs'

pending_jobs_job.title = 'Pending Job'
pending_jobs_job.section = 'shiftleader'

pending_jobs_shift.title = 'Pending Shift'
pending_jobs_shift.section = 'shiftleader'

completed_jobs.title = 'Completed Jobs List'
completed_jobs.section = 'shiftleader'
completed_jobs.page = 'completed_jobs'

completed_detail.title = 'Completed Job Detail'
completed_detail.section = 'shiftleader'

