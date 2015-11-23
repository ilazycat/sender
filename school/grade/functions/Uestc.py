# -*- coding:UTF-8 -*-
__author__ = 'lc4t'

import re
import urllib
import urllib.request
from bs4 import BeautifulSoup
from optparse import OptionParser
import http.cookiejar
from urllib.parse import urlencode
from Uestc2db import DB_uestc
import time
def judgeExistMakeupGrade(gradeList):   #into is tempA, no u'',
    for i in range(0,len(gradeList),8):    # to 8
        if (re.findall(u'--',gradeList[6])):
            return 1
    return 0

class TermStruct:

    def __init__(self):
        self.__length__ = 0
        self.academicYear = []
        self.term = []
        self.numberOfCourses = []
        self.totalCredit = []
        self.gpa = []
        self.all = []
        self.time = []
    def add(self, Academic_Year, Term, Number_Of_Courses, Total_Credit, GPA):
        self.academicYear.append(Academic_Year)
        self.term.append(Term)
        self.numberOfCourses.append(Number_Of_Courses)
        self.totalCredit.append(Total_Credit)
        self.gpa.append(GPA)
        self.__length__ += 1

    def addList(self,list):
        self.academicYear.append(list[0])
        self.term.append(list[1])
        self.numberOfCourses.append(list[2])
        self.totalCredit.append(list[3])
        self.gpa.append(list[4])
        self.__length__ += 1

    def addFinal(self,allGPA,time):
        self.all = allGPA
        self.time = time

    def getFinal(self):
        return [self.all,self.time]

    def printAll(self):
        pass
        # for i in range(0,self.__length__,1):
        #     print (self.academicYear[i],end=' ')
        #     print (u"第",end=' ')
        #     print (self.term[i],end=' ')
        #     print (u"学期 共",end=' ')
        #     print (self.numberOfCourses[i],end=' ')
        #     print (u"门课 总学分",end=' ')
        #     print (self.totalCredit[i],end=' ')
        #     print (u"平均绩点",end=' ')
        #     print (self.gpa[i])

    def printFinal(self):
        # print (u"总课程数:",self.all[0],end=' ')
        # print (u"总学分:",self.all[1],end=' ')
        # print (u"总评绩点:",self.all[2])
        # # print (u"统计时间:",self.time[0])
        pass

    def getTerm(self, number):
        return ([self.academicYear[number], self.term[number], self.numberOfCourses[number],
                 self.totalCredit[number], self.gpa[number]])

    def getCourseNumber(self):
        return self.all[0]

    def getCourseAll(self):
        pass

class Coursestruct:

    def __init__(self):
        self.count = 0
        self.academicYear = []
        self.semester = []
        self.courseCode = []
        self.courseNumber = []
        self.courseName = []
        self.courseType = []
        self.courseCredit = []
        self.courseGrade = []
        self.courseFinal = []
        self.courseGPA = []
        self.makeupGrade = []
        self.isMakeup = 0
    def add(self,course, adjuster, makeup = 0):
        # print (course)
        course[0] = course[0].encode('ascii').decode()
        self.academicYear.append(course[0][1:10])
        self.semester.append(course[0][-1])
        # print (self.semester)

        course[1] = course[1].encode('ascii')
        self.courseCode.append(course[1])
        try:
            course[2] = course[2].encode('ascii')
        except:
            course.insert(2,'###########'.encode('ascii'))
            adjuster = adjuster - 1      # if init course[2] is NULL,there can't encode as 'ascii'

        self.courseNumber.append(course[2])
        self.courseName.append(course[3])

        self.courseType.append(course[4][:-2])

        self.courseCredit.append(course[4][-1])
        # print (course[4][-1])


        if (makeup):
            self.isMakeup = 1
            self.makeupGrade.append(course[6].encode('utf-8').strip())
        else:
            self.makeupGrade.append('')


        try:
            self.courseGrade.append(int(course[5]))
            self.courseFinal.append(int(course[6 + makeup]))
        except:
            if (re.findall(u'未通过',course[5]) != None):
                self.courseGrade.append(0)
                self.courseFinal.append(0)
            elif (re.findall(u'通过',course[5]) != None):
                self.courseGrade.append(100)
                self.courseFinal.append(100)
            else:
                print (u"发现不知名的成绩..")

        if (self.courseGrade[self.count] >= 85):
            self.courseGPA.append(4)
        elif (self.courseGrade[self.count] < 60):
            self.courseGPA.append(1)
        else:
            self.courseGPA.append(4 - (85 - self.courseGrade[self.count]) * 0.1)



        self.count += 1
        return adjuster


    def printCourses(self):
        for i in range(0,self.count, 1):
            print (self.academicYear[i],end=' ')
            print (u"第",end=' ')
            print (self.semester[i],end=' ')
            print (u"学期",end=' ')
            # print (self.courseCode[i],)
            # print (self.courseNumber[i],)
            # print (self.courseType,)
            print (" --> ",)
            print (self.courseName[i].encode('utf-8').decode(),end=' ')
            print (self.courseType[i].encode('utf-8').decode())
            # print ("-------------------------------------------> ",)
            print ("----------------------> ",end=' ')
            print (self.courseCredit[i],end=' ')
            print (u"学分",end=' ')
            print (u"总评",end=' ')
            print (self.courseGrade[i],end=' ')
            print (u"最终",end=' ')
            print (self.courseFinal[i],end=' ')
            print (u"单科绩点",self.courseGPA[i],)
            if (self.isMakeup == 1 and self.makeupGrade[i] != '--'):
                print (u"补考成绩 ",end=' ')
                print (self.makeupGrade[i])
            else:
                print ("")
    def getCoursesJSON(self):

        li = []
        for i in range(0,self.count, 1):
            newDict = {'academisc':self.academicYear[i],
                       'semester':self.semester[i],
                       'courseCode':self.courseCode[i].decode(),
                       'number':self.courseNumber[i].decode(),
                       'courseName':self.courseName[i].encode('utf-8').decode(),
                       'courseType':self.courseType[i].encode('utf-8').decode(),
                       'credit':self.courseCredit[i],
                       'totalGrade':self.courseGrade[i],
                       'makeupGrade':self.makeupGrade[i],
                       'finalGrade':self.courseFinal[i],
                       'gradePoint':self.courseGPA[i]}
            li.append(newDict)

        return li



class GradeAnalyzer:

    def __init__(self,html):
        self.soup = BeautifulSoup(html)

        '''
            griddata-even + griddata-odd 交叉排列
            分别放在list内,
            其中even最后一个是在校汇总,odd最后一个是统计时间

        '''
        self.termData = TermStruct()
        self.coursesData = Coursestruct()

    def printTotal(self):


        self.griddata_even = self.soup.select(".griddata-even")
        self.griddata_odd  = self.soup.select(".griddata-odd")

        self.griddata = []
        for i in range(0, len(self.griddata_even) - 1, 1):
            self.griddata.append(self.griddata_even[i].get_text())
            for j in range(0, len(self.griddata_odd) - 1, 1):
                self.griddata.append(self.griddata_odd[i].get_text())

        for i in range(0,len(self.griddata), 1):
            self.griddata[i] = self.griddata[i].strip('\n').split('\n')
            self.termData.addList(self.griddata[i])

        self.termData.printAll()

        self.griddata = []
        if (len(self.griddata_even) > len(self.griddata_odd)):
            ### 1,3,5,7 term
            self.griddata.append(self.griddata_odd[-1].get_text().encode('ascii','ignore').strip('\n').split('\n'))
            self.griddata.append(self.griddata_even[-1].get_text().encode('ascii','ignore').strip('\n').strip(':').split('\n'))
        else:
            ### 2,4,6,8 term
            # print (self.griddata_even[-1].get_text().encode('ascii','ignore').decode())

            self.griddata.append(self.griddata_even[-1].get_text().encode('ascii','ignore').decode().strip().split())
            self.griddata.append(self.griddata_odd[-1].get_text().encode('ascii','ignore').decode().strip('\n').strip(':').split('\n'))

        self.termData.addFinal(self.griddata[0],self.griddata[1])
        self.termData.printFinal()

    def printCourses(self):
        self.total = self.termData.getCourseNumber()
        self.gridCourses = self.soup.find(id = "grid21344342991_data").get_text()
        temp = re.findall('(?u).*',self.gridCourses)
        tempA = []
        for i in range(0,len(temp),1):
            if (temp[i] == ''):
                continue
            else:
                tempA.append(temp[i])

        isMakeup = judgeExistMakeupGrade(tempA)
        i = 0
        while(i < len(tempA)):
            i = self.coursesData.add(tempA[i:i + 7 + isMakeup],i,isMakeup)
            i += (7 + isMakeup)
        # self.coursesData.printCourses()
        return self.coursesData.getCoursesJSON()

class uestc():
    def __init__(self, username, password):
        self.status = False
        self.loginURL = "http://idas.uestc.edu.cn/authserver/login?service=http://portal.uestc.edu.cn/index.portal"
        self.urlEAS = "http://eams.uestc.edu.cn/eams/home.action"
        self.urlCurriculumManager = "http://eams.uestc.edu.cn/eams/home!childmenus.action?menu.id=844"
        self.urlMygrade = "http://eams.uestc.edu.cn/eams/teach/grade/course/person!historyCourseGrade.action?projectType=MAJOR"
        self.urlCourses = "http://eams.uestc.edu.cn/eams/courseTableForStd!courseTable.action"
        self.loginURLCaptcha = "http://idas.uestc.edu.cn/authserver/needCaptcha.html?username="+username+"&_="+str(time.time())
        self.cookies = http.cookiejar.CookieJar()

        self.headers = {
                'Host': 'idas.uestc.edu.cn',
                'Proxy-Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Origin': 'http://idas.uestc.edu.cn',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'http://idas.uestc.edu.cn/authserver/login?service=http://portal.uestc.edu.cn/index.portal',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.8',
        }



        # proxyConfig = '127.0.0.1:8080'
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies))
        # self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies),urllib.request.ProxyHandler({'http':proxyConfig}))
        # to update self.status
        request_getCookie = urllib.request.Request(url = self.loginURL, headers = self.headers)
        request_need = urllib.request.Request(url = self.loginURLCaptcha, headers = self.headers)



        resulta = self.opener.open(request_getCookie, timeout = 30).read().decode()
        # exit(0)
        # resulta = resulta.decode()
        # assert len(resulta)>100
        resultb = self.opener.open(request_need, timeout = 30).read().decode()
        # print ('need captcha:'+resultb)

        self.lt = re.findall('name="lt" value="(.*)"/>',resulta)[0]

        self.postData = urllib.parse.urlencode(
            {
                'username':username,
                'password':password,
                'lt':str(self.lt),
                'dllt':'userNamePasswordLogin',
                'execution':'e1s1',
                '_eventId':'submit',
                'rmShown':'1'
            }).encode(encoding='UTF8')
        # exit(0)
        self.getIndex()


    #first step to login, this is index page
    def getIndex(self,getter = False):     # login index page



        try:

            request = urllib.request.Request(
                url = self.loginURL,
                data = self.postData,
            )#headers = self.headers)

            result = self.opener.open(request,timeout = 30).read().decode()
            # print (result)
            # requesty = urllib.request.Request(
            #     url = 'http://portal.uestc.edu.cn',)#headers = self.headers)
            # resulty = self.opener.open(requesty, timeout=999).read().decode()
        # except Exception as e:
        #     print (e)
        # try:

            # request = urllib.request.Request(
            #     url = 'http://portal.uestc.edu.cn/index.portal')
            # result = self.opener.open(request, timeout=999).read().decode()
            # print (result)
            # for i in self.cookies:
            #     print (i.name+':'+i.value)

        except Exception as ex:
            # print (Exception, ex)
            self.status = str(ex)
            # return 'Time Out'
        # This is verify mode
        WA = re.findall(u'您提供的用户名或者密码有误',result)
        # WA = False
        AC = re.findall(u'<li>欢迎您：',result)

        if WA or not AC:
            self.status = 'Username or Password wrong'
        else:
            self.status = True
        # print (self.status)
        # Verify mode END
        if (getter):
            return result

        # this is for user to get status
    def getStatus(self):    # to user, return is login success, true: can, false: cannot
        return self.status

    # second step to get course, this is the page after login
    def getEAS(self,getter = False):    #  click educational administration system
        request = urllib.request.Request(url = self.urlEAS)
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies))
        try:
            result = self.opener.open(request,timeout = 30)
        except:
            return 'Time Out'
        if (getter):
            return result.read().decode()

    def getCurriculumManager(self,getter = False):  # table
        request = urllib.request.Request(url = self.urlCurriculumManager)
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies))
        try:
            result = self.opener.open(request,timeout=5)
        except:
            return 'Time Out'
        if (getter):
            return result.read().decode()

    ## after 1, can visit it
    def getMyGrade(self,getter = True):
        request = urllib.request.Request(url = self.urlMygrade)
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies))
        try:
            result = self.opener.open(request,timeout=5)
        except:
            return 'Time Out'
        if (getter):
            return result.read().decode()


def check(username,password):
    user = uestc(username, password)
    return user.getStatus()

def getRawCourse(username,password):
    user = uestc(username, password)
    if (user.getStatus() == True):
        return user.getMyGrade()
    else:
        return 'Authentication failed'

def getCourseList(username,password):
    user = uestc(username, password)
    if (user.getStatus() == True):
        grade = GradeAnalyzer(user.getMyGrade())
        grade.printTotal()
        return grade.printCourses()
    else:
        return 'Authentication failed'


def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser()
    parser.add_option('-u', '--username', help = 'Your username')
    parser.add_option('-p', '--password', help = 'Your password')
    parser.add_option('-f', '--function', help = '1.check: check login.  2.rawCourse: get source of grade page. 3.courseList: get courseList')
    (options, args) = parser.parse_args()
    if (options.username == None or options.password == None or options.function == None):
        parser.print_help()
        exit(0)
    if (options.function == 'check'):
        print (check(options.username,options.password))
    elif (options.function == 'rawCourse'):
        print (getRawCourse(options.username,options.password))
    elif (options.function == 'courseList'):
        print (getCourseList(options.username,options.password))
    else:
        parser.print_help()
    exit(0)


def Exec(username,password,function):
    options = {'username':username,'password':password,'function':function}
    if (function == 'check'):
        return check(username,password)
    elif (function == 'rawCourse'):
        return getRawCourse(username,password)
    elif (function == 'courseList'):
        return getCourseList(username,password)
    else:
        return None

if __name__ == '__main__':
    main()

