# -*- coding:UTF-8 -*-
__author__ = 'lc4t'
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
import datetime
import re
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from kuaidi.models import kuaidiInfo
from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from captcha.models import CaptchaStore
import subprocess
from functions.kuaidi_api import API as kuaidi_api
import json



def Kuaidi(request):
    if not request.user.is_authenticated(): # user is login
        return HttpResponseRedirect('/index/')
    kuaidiList = {}
    if request.POST:
        if ('num' in request.POST and 'comment' in request.POST):

            belongs_id = request.user.id
            num = request.POST.get('num','')
            comment = request.POST.get('comment','')
            # if (len(re.findall('[^a-zA-Z0-9]',num)) > 0 or len(re.findall('[^\u4e00-\u9fa5a-zA-Z0-9]',comment))):
            #     print (num, comment)
            if(not kuaidiInfo.objects.filter(belongs_id = belongs_id, num = num)):### verify repeat
                # try:#userinfo add
                # print (num)
                kuaidi = queryKuaidi(num)
                # print (kuaidi)
                message = kuaidi['message']

                if (kuaidi['verify'] == -1):
                    # return render_to_response('kuaidi.html',{'message':'can not find num'})
                    message = 'Can not find this num'
                elif (kuaidi['verify'] == 0):
                    # NO DATA
                    adder = kuaidiInfo.objects.create(belongs_id = belongs_id, num = kuaidi['num'], company = kuaidi['company'], comment = comment)
                    message = 'No data at this time'
                elif (kuaidi['verify'] == -2):
                else:
                    for one in kuaidi['data']:#TODO sql
                            adder = kuaidiInfo.objects.create(belongs_id = belongs_id, num = kuaidi['num'], company = kuaidi['company'], updateTime = kuaidi['updateTime'], time = one['time'], context = one['context'], comment = comment)
                    message = 'Add success'
                # return render_to_response('kuaidi.html',{'message':'can not find num'})
                # except Exception as e:# error?
                #     print(e)
                #     message = 'Wrong.'
            else:
                message = 'Exists this num.'
    else:# GET
        message = ''
    kuaidiList = kuaidiInfo.objects.filter(belongs_id = request.user.id)
    return render(request, 'kuaidi.html',{'message':message, 'kuaidiList':kuaidiList})


def queryKuaidi(num):
    import requests
    ans = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Referer': 'http://www.kuaidi100.com/',
    }
    if '/' not in num:
        trackingNumber = num
        ans['num'] = trackingNumber
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
    else:
        expressType, trackingNumber = num.split('/')
        ans['company'] = expressType
        ans['num'] = trackingNumber

    getLogisticsURL  = ('http://www.kuaidi100.com/query?type=%s&postid=%s' % (expressType, trackingNumber))
    request = requests.get(getLogisticsURL, headers = headers)
    result = json.loads(request.text)
    ans['message'] = result['message']
    try:
        ans['data'] = result['data']
        ans['updateTime'] = result['data'][0]['ftime']

        ans['verify'] = 1
    except:
            ans['verify'] = -2
        ans['verify'] = 0   # find company, no data
    return ans


def kuaidiRefresh_Ajax(request):
    if request.user.is_authenticated():
        userID = request.user.id
        _ = kuaidi_api()
        message = _.update_id(userID)
        result= {'status':'1','message':str(message)}
    else:
        result= {'status':'0','message':'You are not login'}
    result = json.dumps(result)
    return HttpResponse(result)


def kuaidiDelete(request, ID):
    if not request.user.is_authenticated(): # user is login
        return HttpResponseRedirect('/index/')
    else:
        # kuaidiInfo.objects.filter(id=ID, belongs_id=request.user.id).delete()
        num = kuaidiInfo.objects.filter(id=ID, belongs_id=request.user.id)[0].num
        kuaidiInfo.objects.filter(belongs_id=request.user.id, num=num).delete()
        result= {'status':'0', 'message':'delete ' + ID}
        result = json.dumps(result)
        return HttpResponse(result)
