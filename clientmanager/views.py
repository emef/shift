from shift import render_page, admin_page

@admin_page('clientmanager')
def control_panel(request):
    #list completed jobs awaiting finalization
    return render_page(request, 'clientmanager/control_panel.html')

@admin_page('clientmanager')
def job_new(request):
    return render_page(request, 'clientmanager/job_new.html')

@admin_page('clientmanager')
def job_open(request):
    return render_page(request, 'clientmanager/job_open.html')

@admin_page('clientmanager')
def job_edit(request, job_id):
    return render_page(request, 'clientmanager/job_edit.html')

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

job_edit.title = 'Edit Job'
job_edit.section = 'clientmanager'

job_status.title = 'Job Status'
job_status.section = 'clientmanager'
