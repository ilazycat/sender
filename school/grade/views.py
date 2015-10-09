
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db.models import Q
from grade.models import users
import datetime



def index(request):
    if request.session.get('is_login',False):
        #user not login
        return render_to_response('index.html')

    elif (request.session.get('is_login',True)):
        loginUser = request.session['login_user']
        return render_to_response('index.html')

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

def login(request):
    try:
        m = users.objects.get(username__exact=request.POST['username'])
        if m.password == request.POST['password']:
            request.session['member_id'] = m.id
            return HttpResponse("You're logged in.")
    except users.DoesNotExist:
        return HttpResponse("Your username and password didn't match.")

def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")