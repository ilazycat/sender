
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
import datetime
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from grade.models import grades,userinfo,information
from django import forms
from django.contrib.auth.models import User # 创建用户
from captcha.fields import CaptchaField
from captcha.models import CaptchaStore
from Uestc import Exec
from Uestc2db import DB_uestc
import simplejson
class CaptchaTestForm(forms.Form):
    captcha = CaptchaField()

def filterUsername(raw_username):
    # special permit map: _
    username = re.findall(r'^[a-zA-Z0-9_-]{5,18}$',raw_username)
    if (username):
        return username[0]
    else:
        return False

def filterPassword(raw_password):
    # special permit map: !@$&*,.?_
    password = re.findall(r'^[a-zA-Z0-9!@$&*,.?_-]{6,18}$',raw_password)
    if (password):
        return password[0]
    else:
        return False

def filterEmail(raw_email):
    # special permit map: !@$&*,.?_
    email = re.findall(r'^[a-zA-Z0-9._-]+\@[a-zA-Z0-9_-]+\.[a-zA-Z0-9._-]+$',raw_email)
    if (email):
        return email[0]
    else:
        return False

def query(table):
    return eval(table+'.objects')


def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html',{'current_datetime':now})

def hours_ahead(request, offset):
    offset = int(offset)
    dt = datetime.datetime.now() + datetime.timedelta(hours = offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)



def Index(request):
# the index page for all
    if request.user.is_authenticated():
        return render_to_response('index.html',{'title':'hello '+request.user.username})
    return render_to_response('index.html',{'title':'hello~~~~'})

def Register(request):

    # TODO:  vcode for same ip many times
    # TODO:  Bootstrap Validator

    #filter the input
    ### POST > vcode > input
    messageType = 'danger'      # default
    if request.POST:
        form = CaptchaTestForm(request.POST)
        if form.is_valid():
            human = True
            message = 'code was true, no input'
            if ('username' in request.POST and 'password' in request.POST and 'email' in request.POST):
                username = filterUsername(request.POST.get('username',''))
                password = filterPassword(request.POST.get('password',''))
                email    = filterEmail(request.POST.get('email',''))
                try:
                    if (username and password and email):
                        user = User.objects.create_user(username, email, password)
                        messageType = 'success'
                        message = 'code was true,user can add'
                        user = authenticate(username=username, password=password)
                        login(request, user)
                        return HttpResponseRedirect('/home/')
                    else:
                        # print (username,password,email)
                        message = 'Please check your input,May not in permission'
                except:
                    message = 'code was true, user can not add'
        else:
            message = 'code was wrong'
    else:
        form = CaptchaTestForm()
        messageType = 'info'
        message = 'No input'
    ### this is beauty the captcha input

    # img_src = captcha['pic']['src']
    # input1_value = captcha['input1']['value']
    # 'img_src':img_src, 'input1_value':input1_value,
    return render_to_response('register.html', {'captcha':form, 'messageType':messageType,'message':message},context_instance=RequestContext(request))



def Login(request):
    message = None
    if request.user.is_authenticated():# had login
        return HttpResponseRedirect('/home/')
    if request.POST:
        form = CaptchaTestForm(request.POST)
        if form.is_valid():
            human = True
            if ('username' in request.POST and 'password' in request.POST):
                username = filterUsername(request.POST.get('username',''))
                password = filterPassword(request.POST.get('password',''))
                user = authenticate(username=username, password=password)
                if user is not None:# no this user
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect('/home/') #login success
                    else:# user not active
                        message = 'username' + ' is not active.'
                else:#password wrong
                    message = 'username and password are not match.'
            else:#no username,password value
                message = 'What are you doing?'
    else:# GET
        form = CaptchaTestForm()
    return render_to_response('login.html',{'captcha':form,'message':message},context_instance=RequestContext(request))



def Logout(request):
    logout(request)
    return HttpResponseRedirect('/index/')


def Home(request):
    # @login_required
    if request.user.is_authenticated():
        return render_to_response('home.html',{'title':request.user.username+'\'s home page','user':request.user.username, 'active_home':'active'},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/index/')







def Manage(request):
    if request.user.is_authenticated():
        verifyFull(request.user.id)
        userinfoList = userinfo.objects.filter(belongs_id = request.user.id)
        return render_to_response('manage.html',{'user':request.user.username, 'active_manage':'active', 'userinfoList':userinfoList})
    else:
        return HttpResponseRedirect('/login/')

## TODO: manage

def Add(request):   #add an account for manage
    if not request.user.is_authenticated(): # user is login
        return HttpResponseRedirect('/login/')
    ####EDITING
    message = None
    if request.POST:
        form = CaptchaTestForm(request.POST)
        if form.is_valid():
            human = True
            if ('username' in request.POST and 'password' in request.POST  and 'school' in request.POST):
                belongs_id = request.user.id
                username   = request.POST.get('username','')
                password   = request.POST.get('password','')
                email      = request.POST.get('email','')
                school     = request.POST.get('school','')
                if(not userinfo.objects.filter(belongs_id = belongs_id, username = username, school = school)):### verify repeat
                    try:#userinfo add
                        adder = userinfo.objects.create(belongs_id = belongs_id , username = username, password= password, email = email, school = school, verify = False)
                        return HttpResponseRedirect('/manage/')
                    except:# error?
                        message = 'This user cannot add.'
                else:#had added
                    message = 'You had added this account.'
            else:#no username,password value
                message = 'What are you doing?'
    else:# GET
        form = CaptchaTestForm()
    return render_to_response('add.html',{'captcha':form,'message':message, 'active_add':'active'},context_instance=RequestContext(request))

def verifyOne(belongs_id,username,password,school):
    users = userinfo.objects.filter(belongs_id = belongs_id, username = username, password = password, school = school,verify = False)
    for user in users:
        if (school == 'uestc'):
            status = Exec(username,password,'check')
            if (status == True):
                user = userinfo.objects.filter(username = username, password = password, school = school).update(verify = True)
            else:
                pass
        ### elif other school
        else:
            return False

def VerifyFull_Ajax(request):
    # there should return an alert to user: reload
    if request.user.is_authenticated():
        verifyFull(request.user.id)
        result = '1'
    else:
        result= '0'
    result = simplejson.dumps(result)
    return HttpResponse(result)


def verifyFull(belongs_id = 0):
    #this is verify by login_user,not decided by post
    users = userinfo.objects.filter(belongs_id = belongs_id)
    for user in users:
        if user.verify:
            continue
        else:
            print ('verify:'+user.username)
            verifyOne(belongs_id, user.username, user.password, user.school)



def Change(request):
    return HttpResponseRedirect('/Add/')




def Delete(request):
    if not request.user.is_authenticated(): # user is login
        return HttpResponseRedirect('/login/')
    else:
        pass

