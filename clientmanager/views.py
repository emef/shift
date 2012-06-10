from pprint import pprint

from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from shift import render_page, admin_required, json_response
from shift.clientmanager.forms import JobForm, ShiftForm, mk_role_forms
from shift.jobs.models import Job, Shift
from shift.users.models import ContractorRole

import simplejson

@admin_required('clientmanager')
def control_panel(request):
    #list completed jobs awaiting finalization
    return render_page(request, 'clientmanager/control_panel.html')

@admin_required('clientmanager')
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

@admin_required('clientmanager')
def job_open(request):
    data = {'jobs': Job.objects.all()}
    return render_page(request, 'clientmanager/job_open.html', data)

@admin_required('clientmanager')
def job_edit(request, job_id):
    if request.method == 'POST':
        return ajax_job_edit(request, job_id)

    job = get_object_or_404(Job, pk=job_id)
    job_form = JobForm(instance=job)
    shift_form = ShiftForm()

    existing_shifts = [{'title': s.title,
                        'form': ShiftForm(instance=s),
                        'roles': mk_role_forms(s)} for s in job.shifts.all()]

    # INCORPORATE EXISTING SHIFT DATA
    
    data = {'job_title': job.title,
            'job_form': job_form,
            'existing_shifts': existing_shifts,
            'empty_roles': mk_role_forms(),
            'empty_shift': shift_form,
    }
    
    return render_page(request, 'clientmanager/job_edit.html', data)

def ajax_job_edit(request, job_id):
    job = get_object_or_404(Job, pk=job_id)

    json = simplejson.loads(request.POST['json'])
    job = get_object_or_404(Job, pk=job_id)
    job_form = JobForm(json['basic'], instance=job)
    job = job_form.save(commit=False)

    existing = dict( (s.id, s) for s in job.shifts.all() )
    
    errors = {}
    
    for shift_json in json['shifts']:
        shift_form = ShiftForm(shift_json['info'])
        if not shift_form.is_valid():
            title = shift_form.data['title']
            errors[title] = ['{0}: {1}'.format(f, e[0]) for f,e in shift_form.errors.items()]
            break
            
        shift = shift_form.save(commit=False)
        shift.job = job
        
        id = shift_form.cleaned_data['id']
        if id in existing:
            shift.id = id
            del existing[id]
            
        shift.save()

        filter_errors = shift.update_filters(shift_json['attrs'])

        if len(filter_errors) > 0:
            errors[shift.title] = filter_errors
            
    Shift.objects.filter(id__in=existing.keys()).delete()
        
    if len(errors) == 0:
        return json_response({'status': 'ok'})
    else:
        return json_response({'status': 'error',
                              'errors': errors})

@admin_required('clientmanager')
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
