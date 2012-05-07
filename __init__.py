from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404

import simplejson as json

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

def admin_page(group=None):
    def _dec(view_func):
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
