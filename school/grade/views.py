
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db.models import Q
from grade.models import users
from django.contrib import auth
import datetime



def index(request):
    # if request.session.get('is_login',False):
    #     return render_to_response('index.html',{'title':'Hello'})
    # elif (request.session.get('is_login',True)):
    #     return render_to_response('index.html',{'title':'Hello guy'})
    # else:
    #     return render_to_response('index.html',{'title':'Hello'})
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



from django.contrib.auth import authenticate, login


def Login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
