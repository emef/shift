from django.http import Http404
from shift import render_page, admin_page
from shift.talentmanager.forms import ExcelUploadForm

@admin_page('talentmanager')
def control_panel(request):
    form = ExcelUploadForm()
    data = {'form': form}
    return render_page(request, 'talentmanager/control_panel.html', data)

@admin_page('talentmanager')
def upload(request):
    if request.method != 'POST':
        raise Http404
    form = ExcelUploadForm(request.POST, request.FILES)
    if not form.is_valid():
        data = {'form': form}
        return render_page(request, 'talentmanager/control_panel.html', data)
    else:
        return control_panel(request)
        
    


control_panel.title = 'Talent Manager Control Panel'
control_panel.section = 'talentmanager'

upload.title = 'Upload Contractor Info'
upload.section = 'talentmanager'
