from django import forms
from django.db import models
from django.utils.safestring import mark_safe
from django.conf import settings
from random import random

DEFAULT_WIDTH = 300
DEFAULT_HEIGHT = 200

DEFAULT_LAT = 55.16
DEFAULT_LNG = 61.4

LOCATION_HTML_FMT=u"""\
<div>
    {0}
    <div id="{1}" class='googlemap' style='width:{2}px; height:{3}px'></div>
</div>
"""

class LocationWidget(forms.TextInput):
    def __init__(self, *args, **kw):

        self.map_width = kw.get("map_width", DEFAULT_WIDTH)
        self.map_height = kw.get("map_height", DEFAULT_HEIGHT)

        super(LocationWidget, self).__init__(*args, **kw)
        self.inner_widget = forms.widgets.HiddenInput()

    def render(self, name, value, *args, **kwargs):
        if value is None:
            lat, lng = DEFAULT_LAT, DEFAULT_LNG
        else:
            if isinstance(value, unicode):
                a, b = value.split(',')
            else:
                a, b = value
            lat, lng = float(a), float(b)

        doc_id = 'id_{0}_{1}'.format(name, random()*100000)
        widget_html = self.inner_widget.render(name, 
                                               "%f,%f" % (lat, lng), 
                                               {'id':'%s' % doc_id})
        
        html = LOCATION_HTML_FMT.format(widget_html, doc_id+'_map', self.map_width, self.map_height)
        
        return mark_safe(html)

    class Media:
        js = ('{0}js/googlemaps_widget.js'.format(settings.STATIC_URL), 
              'http://maps.google.com/maps/api/js?sensor=false',)

class LocationFormField(forms.CharField):
    def clean(self, value):
        if isinstance(value, unicode):
            a, b = value.split(',')
        else:
            a, b = value

        lat, lng = float(a), float(b)
        return "%f,%f" % (lat, lng)

class LocationField(models.CharField):
    def formfield(self, **kwargs):
        defaults = {'form_class': LocationFormField}
        defaults.update(kwargs)
        defaults['widget'] = LocationWidget
        return super(LocationField, self).formfield(**defaults)
