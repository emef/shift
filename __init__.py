from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

import re
import simplejson as json

def _choice_assoc_fn(x, choices, keyfn):
    for item in choices:
        key, val = item
        
        # nested choices
        if isinstance(val, tuple):
            for subkey, subval in val:
                found = keyfn(x, subkey, subval)
                if found != None:
                    return found
                
        # single choice
        else:
            found = keyfn(x, key, val)
            if found != None:
                return found

def choice_assoc(x, choices):
    def keyfn(x, key, val):
        if x == key:
            return val
    return _choice_assoc_fn(x, choices, keyfn)

def choice_rassoc(x, choices):
    def keyfn(x, key, val):
        if x == val:
            return key
    return _choice_assoc_fn(x, choices, keyfn)
        
def render_page(request, template_name, *args):
    output = args[0] if len(args) > 0 else {}
    if hasattr(request, 'page_info'):
        output['page_info'] = request.page_info
        output['page_info']['path'] = request.path
    return render_to_response(template_name, output, context_instance=RequestContext(request))

def contains(obj, *args):
    return all (k in obj for k in args)

def extract(obj, *args):
    lst = []
    for key in args:
        lst.append(obj.get(key, None))
    return tuple(lst)

def json_response(resp):
    return HttpResponse(json.dumps(resp), mimetype="application/json")

def admin_required(group=None):
    def _dec(view_func):
        @login_required
        def _view(request, *args, **kwargs):
            if group and not group in set([g.name for g in request.user.groups.all()]):
                raise Http404
            request.page_info = {'title': view_func.title,
                                 'section': view_func.section,
                                 'page': getattr(view_func, 'page', None) }
            return view_func(request, *args, **kwargs)
        
        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__
    
        return _view
    
    return _dec

height_inches = re.compile(r"(\d+')(\d+\")?")

def from_measurement(measurement):
    m = height_inches.match(measurement)
    if m:
        val = 0
        for mval in m.groups():
            if mval[-1] == '"':
                val += int(mval[:-1])
            elif mval[-1] == "'":
                val += 12 * int(mval[:-1])
        return val
    else:
        return measurement
