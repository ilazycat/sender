from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    # html = "<html><body>It is now %s.</body></html>" % now
    # return HttpResponse(html)
    t = get_template('current_date.html')
    html = t.render(Context({'current_date':now}))
    return HttpResponse(html)


def hours_ahead(request, offset):
    offset = int(offset)
    dt = datetime.datetime.now() + datetime.timedelta(hours = offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)