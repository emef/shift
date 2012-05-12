from pprint import pprint

from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from shift import render_page, admin_page
from shift.clientmanager.forms import JobForm, ShiftForm, mk_attribute_form
from shift.jobs.models import Job, Shift
from shift.users.models import AttributeSet

@admin_page('clientmanager')
def control_panel(request):
    #list completed jobs awaiting finalization
    return render_page(request, 'clientmanager/control_panel.html')

@admin_page('clientmanager')
def job_new(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save()
            return redirect('/client-manager/job/edit/{0}'.format(job.id))
    else:
        form = JobForm()
        
    data = {'form': form}
    return render_page(request, 'clientmanager/job_new.html', data)

@admin_page('clientmanager')
def job_open(request):
    data = {'jobs': Job.objects.all()}
    return render_page(request, 'clientmanager/job_open.html', data)

@admin_page('clientmanager')
def job_edit(request, job_id):
    job = get_object_or_404(Job, pk=job_id)

    #stub
    if request.method == 'POST':
        pass
    else:
        job_form = JobForm(instance=job)
        shift_form = ShiftForm()

    existing_shifts = [{'title': s.title,
                        'form': ShiftForm(instance=s)} for s in job.shifts.all()]

    att_form = mk_attribute_form()
    
    data = {'job_title': job.title,
            'job_form': job_form,
            'empty_shift': shift_form,
            'existing_shifts': existing_shifts,
            'attribute_form': att_form}
    return render_page(request, 'clientmanager/job_edit.html', data)

@admin_page('clientmanager')
def job_status(request, job_id):
    return render_page(request, 'clientmanager/job_status.html')

control_panel.title = 'Client Manager Control Panel'
control_panel.section = 'clientmanager'

job_new.title = 'Create Job'
job_new.section = 'clientmanager'
job_new.page = 'job_new'

job_open.title = 'Open Job'
job_open.section = 'clientmanager'
job_open.page = 'job_open'

job_edit.title = 'Edit Job'
job_edit.section = 'clientmanager'

job_status.title = 'Job Status'
job_status.section = 'clientmanager'
