from pprint import pprint
from django.shortcuts import redirect
from django.http import Http404
from django.contrib.auth.models import User
from shift import render_page, admin_required
from shift.talentmanager.forms import GoogleDocForm
from shift.users.models import Contractor, Attribute, ContractorAttributeVal
from shift.shift_settings import attr_info

import shift.shift_settings as settings
import datetime

import gdata.docs
import gdata.docs.service
import gdata.spreadsheet.service

@admin_required('talentmanager')
def control_panel(request):
    form = GoogleDocForm()
    data = {'form': form}
    return render_page(request, 'talentmanager/control_panel.html', data)

@admin_required('talentmanager')
def upload(request):
    if request.method != 'POST':
        raise Http404
    form = GoogleDocForm(request.POST, request.FILES)
    if not form.is_valid():
        data = {'form': form}
        return render_page(request, 'talentmanager/control_panel.html', data)
    else:
        # Connect to Google
        gd_client = gdata.spreadsheet.service.SpreadsheetsService()
        gd_client.email = form.cleaned_data['google_username']
        gd_client.password = form.cleaned_data['google_password']
        gd_client.source = 'shift.ttforbes.com'
        gd_client.ProgrammaticLogin()
        
        q = gdata.spreadsheet.service.DocumentQuery()
        q['title'] = form.cleaned_data['document_name']
        #q['title-exact'] = 'true'
        feed = gd_client.GetSpreadsheetsFeed(query=q)
        spreadsheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
        feed = gd_client.GetWorksheetsFeed(spreadsheet_id)
        worksheet_id = feed.entry[0].id.text.rsplit('/',1)[1]

        rows = gd_client.GetListFeed(spreadsheet_id, worksheet_id).entry

        def shorthand(key): return key.replace(' ', '').lower()
        
        attrs = dict((shorthand(a.field_name), a) for a in Attribute.objects.all())
        
        errors = []
        
        for row in rows:
            # get the contractor if he/she exists
            firstname = row.custom['firstname'].text
            lastname = row.custom['lastname'].text
            contact_email = row.custom['contactemail'].text
            payment_email = row.custom['paymentemail'].text
            phone = row.custom['phone'].text
            location = row.custom['location'].text
            m,d,y = row.custom['birthdate'].text.split('/')
            birthdate = datetime.date(int(y), int(m), int(d))

            # get Contractor object
            try:
                contractor = Contractor.objects.get(user__first_name=firstname,
                                                    user__last_name=lastname)
            except Contractor.DoesNotExist:
                user = User.objects.create(first_name=firstname,
                                           last_name=lastname,
                                           username=contact_email,
                                           email=contact_email)
                contractor = Contractor(user=user)
                
            # populate/update contractor info
            contractor.birthdate = birthdate
            contractor.contact_email = contact_email
            contractor.payment_email = payment_email
            contractor.phone = phone
            contractor.location = location
            contractor.user.email = contact_email
            contractor.user.username = contact_email
            contractor.save()

            full_name = '{0} {1}'.format(firstname, lastname)
            
            # blow away old attributes
            contractor.attributes.all().delete()
            
            vals = []
            local_errors = []
            
            for key in row.custom:
                cell = row.custom[key].text
                if key in attrs and cell != None:
                    try:
                        attr = attrs[key]
                        val = attr.mk_val(cell)
                        val.contractor = contractor
                        vals.append(val)
                    except:
                        local_errors.append('Could not set {0} = {1}'.format(key,cell))
                
            ContractorAttributeVal.objects.bulk_create(vals)

            if len(local_errors) > 0:
                errors.append({'contractor': full_name,
                               'errors': local_errors})
                
        data = {'form': form}
        if len(errors) > 0:
            data['errors'] = errors
        else:
            data['success'] = 1
            
        return render_page(request, 'talentmanager/control_panel.html', data)
    
    


control_panel.title = 'Talent Manager Control Panel'
control_panel.section = 'talentmanager'

upload.title = 'Upload Contractor Info'
upload.section = 'talentmanager'
