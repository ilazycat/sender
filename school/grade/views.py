
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from grade.models import users
from django.contrib import auth
import datetime
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def index(request):
    return render_to_response('index.html',{'title':'hello~~~~'})
def register(request):
    return render_to_response('register.html')

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html',{'current_datetime':now})

def hours_ahead(request, offset):
    offset = int(offset)
    dt = datetime.datetime.now() + datetime.timedelta(hours = offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

def search(request):
    query = request.GET.get('q','')
    if query:
        qset = (
            Q(username__contains=query) |
            Q(email__contains=query)
        )
        results = users.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response('search.html',{
        "results":results,
        "query":query
        })






def Login(request):
    # assert False
    if ('username' in request.POST and 'password' in request.POST):
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/home/?username='+username)
            else:
                return render_to_response('login.html',{"errormessage":username+" is not active."}, context_instance=RequestContext(request))
        else:
            return render_to_response('login.html',{"errormessage":"username and password are not match."}, context_instance=RequestContext(request))
    else:
        return render_to_response('login.html',{"errormessage":"Please login in."}, context_instance=RequestContext(request))