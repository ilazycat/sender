# -*- coding:UTF-8 -*-
__author__ = 'lc4t'
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
import datetime
import re
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from grade.models import grades,userinfo,information,kuaidiInfo
from django import forms
from django.contrib.auth.models import User # 创建用户
from captcha.fields import CaptchaField
from captcha.models import CaptchaStore
import subprocess
from Uestc import Exec
from AutoCheckKuaidi import Refresh
from Uestc2db import DB_uestc
import simplejson
class CaptchaTestForm(forms.Form):
    captcha = CaptchaField()

def filterUsername(raw_username):
    # special permit map: _
    username = re.findall(r'^[a-zA-Z0-9_-]{4,18}$',raw_username)
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
        return render_to_response('home.html',{'title':request.user.username+'\'s home page','user':request.user.username, 'active_home':'active', 'active_kuaidi':'active'},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/index/')







def Manage(request):
    if request.user.is_authenticated():
        userinfoList = userinfo.objects.filter(belongs_id = request.user.id)
        return render_to_response('manage.html',{'user':request.user.username, 'active_manage':'active', 'userinfoList':userinfoList})
    else:
        return HttpResponseRedirect('/login/')



def Grade(request):

    if request.user.is_authenticated():
        userinfoList = userinfo.objects.filter(belongs_id = request.user.id)
        return render_to_response('grade.html',{'user':request.user.username, 'active_manage':'active', 'userinfoList':userinfoList})
    else:
        return HttpResponseRedirect('/login/')
#TODO : NO function to this

def Userinfo(request, userinfoID):
    #TODO: select what user wants, check the grades here
    if request.user.is_authenticated():
        userinfoList = userinfo.objects.filter(id = userinfoID)
        gradeList = grades.objects.filter(belongs_id = userinfoID)
        return render_to_response('userinfo.html',{'user':request.user.username, 'active_manage':'active', 'userinfoList':userinfoList, 'gradeList':gradeList,'oneDay':((datetime.datetime.now() - datetime.timedelta(days = 1))).strftime("%Y-%m-%d %H:%M:%S")})
    else:
        return HttpResponseRedirect('/login/')

def userInfoAddGrade_Ajax(request, userinfoID = 0):
    # print (userinfoID)
    if request.user.is_authenticated():
        # try:
        user = userinfo.objects.filter(id = userinfoID)[0]
        if user.verify == True:
            li = Exec(user.username, user.password, 'courseList')
            db = DB_uestc(userinfoID, os.getcwd() + '/data.db')
            db.sync(li)
            result= {'status':'1','message':'sync done'}
        else:
            result= {'status':'0','message':'Not Verify Account'}
    else:
        result= {'status':'0','message':'You are not login'}
    result = simplejson.dumps(result)
    return HttpResponse(result)







def Add(request):   #add an account for manage
    if not request.user.is_authenticated(): # user is login
        return HttpResponseRedirect('/login/')
    ####EDITING
    username   = ''
    password   = ''
    email      = ''
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
        else:
            message = 'code was wrong'
    else:# GET
        form = CaptchaTestForm()
    return render_to_response('add.html',{'captcha':form,'message':message, 'username':username, 'password':password, 'email':email, 'active_add':'active', 'active_kuaidi':'active'},context_instance=RequestContext(request))

def userInfoverifyOne(belongs_id,username,password,school):
    users = userinfo.objects.filter(belongs_id = belongs_id, username = username, password = password, school = school,verify = False)
    for user in users:
        if (school == 'uestc'):
            try:
                status = Exec(username,password,'check')
            except Exception as e:
                status = e
            if (status == True):
                user = userinfo.objects.filter(username = username, password = password, school = school).update(verify = True)
                return True
            else:
                return status
        ### elif other school
        else:
            return 'No this school'

def userInfoVerifyFull_Ajax(request):
    # there should return an alert to user: reload
    if request.user.is_authenticated():
        message = userInfoverifyFull(request.user.id)
        result= {'status':'1','message':str(message)}
    else:
        result= {'status':'0','message':'You are not login'}
    result = simplejson.dumps(result)
    return HttpResponse(result)


def userInfoverifyFull(belongs_id = 0):
    #this is verify by login_user,not decided by post
    users = userinfo.objects.filter(belongs_id = belongs_id)
    result = []
    for user in users:
        # print (user)
        if user.verify:
            result.append(True)
        else:
            # print ('verify:'+user.username)
            result.append(userInfoverifyOne(belongs_id, user.username, user.password, user.school))
    return result



def userInfoChange(request, userinfoID):
    if not request.user.is_authenticated(): # user is login
        return HttpResponseRedirect('/login/')
    ####EDITING
    message = None
    users = userinfo.objects.filter(id = userinfoID)[0]

    try:
        if (request.user.id == users.belongs_id):
            username = users.username
            password = users.password
            email = users.email
            school = users.school
        else:
            # NO permission
            result= {'status':'-1', 'message':'No permission' }
            result = simplejson.dumps(result)
            return HttpResponse(result)
    except Exception as e:
        result= {'status':'-1', 'message':'something was wrong' }
        result = simplejson.dumps(result)
        return HttpResponse(result)



    if request.POST:
        form = CaptchaTestForm(request.POST)
        if form.is_valid():
            human = True
            if ('username' in request.POST and 'password' in request.POST  and 'school' in request.POST):
                username   = request.POST.get('username','')
                password   = request.POST.get('password','')
                email      = request.POST.get('email','')
                school     = request.POST.get('school','')
                try:#userinfo change
                    users.username = username
                    users.password = password
                    users.email = email
                    users.school = school
                    users.save()
                    return HttpResponseRedirect('/manage/')
                except:# error?
                    message = 'This user cannot change.'
            else:#no username,password value
                message = 'What are you doing?'
        else:
            message = 'code was wrong'
    else:# GET
        form = CaptchaTestForm()
    return render_to_response('change.html',{'username':username, 'password':password, 'email':email, 'school':school, 'captcha':form,'message':message, 'active_add':'active'},context_instance=RequestContext(request))





def userInfoDelete(request, userinfoID):
    if not request.user.is_authenticated(): # user is login
        return HttpResponseRedirect('/login/')
    else:
        userinfo.objects.filter(id = userinfoID).delete()
        result= {'status':'0', 'message':'delete ' + userinfoID}
        result = simplejson.dumps(result)
        return HttpResponse(result)


def Kuaidi(request):
    if not request.user.is_authenticated(): # user is login
        return HttpResponseRedirect('/login/')
    kuaidiList = {}
    if request.POST:
        if ('num' in request.POST and 'comment' in request.POST):
            
            belongs_id = request.user.id
            num = request.POST.get('num','')
            comment = request.POST.get('comment','')
            if (len(re.findall('[^a-zA-Z0-9]',num)) > 0 or len(re.findall('[^\u4e00-\u9fa5a-zA-Z0-9]',comment))):
                print (num, comment)
                exit(0)
            if(not kuaidiInfo.objects.filter(belongs_id = belongs_id, num = num)):### verify repeat
                try:#userinfo add
                    print (num)
                    kuaidi = queryKuaidi(num)
                    print (kuaidi)
                    message = kuaidi['message']
                    
                    if (kuaidi['verify'] == -1):
                        # return render_to_response('kuaidi.html',{'message':'can not find num'},context_instance=RequestContext(request))
                        message = 'Can not find this num'
                    elif (kuaidi['verify'] == 0):
                        # NO DATA
                        adder = kuaidiInfo.objects.create(belongs_id = belongs_id, num = kuaidi['num'], company = kuaidi['company'], comment = comment)
                        message = 'Num exists, nut no data'
                    else:
                        for one in kuaidi['data']:#TODO sql
                                adder = kuaidiInfo.objects.create(belongs_id = belongs_id, num = kuaidi['num'], company = kuaidi['company'], updateTime = kuaidi['updateTime'], time = one['time'], context = one['context'], comment = comment)
                        message = 'Add success'
                    # return render_to_response('kuaidi.html',{'message':'can not find num'},context_instance=RequestContext(request))
                except Exception as e:# error?
                    if (DEBUG):
                        print (e)
                    message = 'Wrong.'
            else:
                message = 'Exists this num.'
    else:# GET
        message = ''
    kuaidiList = kuaidiInfo.objects.filter(belongs_id = request.user.id)
    print (kuaidiList)
    return render_to_response('kuaidi.html',{'message':message, 'kuaidiList':kuaidiList},context_instance=RequestContext(request))


def queryKuaidi(num):
    import requests
    ans = {}
    trackingNumber = num
    ans['num'] = trackingNumber
    headers = {
        'Accept' : 'application/json, text/plain, */*',
        'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8',
        'Referer' : 'http://www.kuaidi100.com/',
    }
    getExpressURL = ('http://www.kuaidi100.com/autonumber/autoComNum?text=%s' % trackingNumber)
    request = requests.get(getExpressURL, headers = headers)
    result = eval(str(request.text))
    try:
        expressType = result['auto'][0]['comCode']
        ans['company'] = expressType
    except:
        ans['verify'] = -1
        ans['message'] = 'bad input, can not find company or no this code'
        return ans
    getLogisticsURL  = ('http://www.kuaidi100.com/query?type=%s&postid=%s' % (expressType, trackingNumber))
    request = requests.get(getLogisticsURL, headers = headers)
    result = eval(str(request.text))
    ans['message'] = result['message']
    try:
        ans['data'] = result['data']
        ans['updateTime'] = result['data'][0]['ftime']

        ans['verify'] = 1
    except:
        ans['verify'] = 0   # find company, no data
    return ans


def kuaidiRefresh_Ajax(request):
    if request.user.is_authenticated():
        userID = request.user.id
        message = Refresh(userID)
        result= {'status':'1','message':str(message)}
    else:
        result= {'status':'0','message':'You are not login'}
    result = simplejson.dumps(result)
    return HttpResponse(result)


def kuaidiDelete(request, ID):
    if not request.user.is_authenticated(): # user is login
        return HttpResponseRedirect('/login/')
    else:
        kuaidiInfo.objects.filter(id = ID).delete()
        result= {'status':'0', 'message':'delete ' + ID}
        result = simplejson.dumps(result)
        return HttpResponse(result)

