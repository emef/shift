from django.core.mail import EmailMessage

ABSOLUTE_DOMAIN = 'http://shift.ttforbes.com'
CONFIRM_URL = 'http://{0}/shift/confirm/{1}/'
UNCONFIRM_URL = 'http://{0}/shift/unconfirm/{1}'

def confirm_url(uid): return CONFIRM_URL.format(ABSOLUTE_DOMAIN, uid)
def unconfirm_url(uid): return UNCONFIRM_URL.format(ABSOLUTE_DOMAIN, uid)

def send_confirmation_email(assignment):
    html = '''Please confirm your availability for the following shift:
Title: {title}
Role: {role}
Starts: {starts}
Ends: {ends}
Pays: {pays}
Location: {location}

<a href='{confirm_url}'>Yes, I can make this shift</a>
<a href='{unconfirm_url}'>No, I can not make this shift</a>

Thanks,
ShiftTalent'''.format(
            title=assignment.shift.title,
            role=assignment.shift.role,
            starts=assignment.shift.start,
            ends=assignment.shift.end,
            pays=assignment.shift.pays,
            location=assignment.shift.location,
            confirm_url=confirm_url(assignment.uid),
            unconfirm_url=unconfirm_url(assignment.uid)
            ).replace('\n', '<br />\n')

    to = [assignment.contractor.contact_email]
    msg = EmailMessage('ShiftTalent: Availability Confirmation', html, to=to)
    msg.content_subtype = 'html'
    msg.send()
