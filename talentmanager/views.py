from django.shortcuts import redirect
from django.http import Http404
from shift import render_page, admin_required
from shift.talentmanager.forms import ExcelUploadForm

import gdata.gauth
import gdata.docs.client

# google authentication url
def GetAuthSubUrl(next):
    scopes = ['http://docs.google.com/feeds/', 'https://docs.google.com/feeds/']
    secure = False  # set secure=True to request a secure AuthSub token
    session = True
    return gdata.gauth.generate_auth_sub_url(next, scopes, secure=secure, session=session)

@admin_required('talentmanager')
def control_panel(request):
    url = GetAuthSubUrl(str(request.build_absolute_uri('/talent-manager/upload/')))
    return redirect(str(url))
    form = ExcelUploadForm()
    data = {'form': form}
    return render_page(request, 'talentmanager/control_panel.html', data)

@admin_required('talentmanager')
def upload(request):
    import pprint
    pprint.pprint(request.GET['token'])
    client = gdata.docs.client.DocsClient()
    client.GetAccessToken(request.GET['token'])
    pprint.pprint(client.GetResources())
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
