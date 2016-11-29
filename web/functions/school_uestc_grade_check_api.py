import sqlite3
import datetime
import re
import time
import threading
from optparse import OptionParser
from .school_uestc_grade_get_api import API as uestc
from .get_contact_api import API as contact

class DB:
    def __init__(self, db = 'data.db'):
        self.cx = sqlite3.connect(db)
        self.cu = self.cx.cursor()
        self.Grade_Grades = 'school_grades'
        self.Grade_Userinfo = 'school_userinfo'
    def getNewUestc(self, minutes = 10):
        timeStr = ((datetime.datetime.now() - datetime.timedelta(minutes = minutes)).strftime('%Y-%m-%d %H:%M:%S'))
        sql = ("select * from %s where updateTime>'%s'" % (self.Grade_Grades, timeStr))
        self.cu.execute(sql)
        # print (sql)
        return self.cu.fetchall()
    def getUsername(self, belongs_id = 0):
        if (belongs_id <= 0):
            return None
        sql = ("select username from %s where id=%d" % (self.Grade_Userinfo, belongs_id))
        self.cu.execute(sql)
        response = self.cu.fetchall()
        return response[0][0]

    def getNewUestcByID(self, belongs_id = 0, minutes = 10):
        timeStr = ((datetime.datetime.now() - datetime.timedelta(minutes = minutes)).strftime('%Y-%m-%d %H:%M:%S'))
        sql = ("select courseName,courseType,credit,totalGrade,finalGrade,gradePoint,updateTime from %s where belongs_id='%s' and updateTime>'%s'" % (self.Grade_Grades, belongs_id, timeStr))
        self.cu.execute(sql)
        response = self.cu.fetchall()
        result = []
        result.append('Username:' + str(self.getUsername(belongs_id)) + '\n')
        for one in response:
            result.append(Convert2Text(one))
        return '-----------\n'.join(result)
    def getEmailByID(self, userID):
        sql = ("select email from %s where id=%d" % (self.Grade_Userinfo, int(userID)))
        self.cu.execute(sql)
        response = self.cu.fetchone()
        return re.split(',| ', response[0]) # list
    def getUsersBySchool(self, school = 'uestc'):
        sql = ("select id from %s where school='%s'" % (self.Grade_Userinfo, school))
        self.cu.execute(sql)
        response = self.cu.fetchall()
        result = []
        for one in response:
            result.append(one[0])
        return result
    def getUsernameAndPasswordByID(self, userID):
        sql = ("select username,password,verify from %s where id=%d" % (self.Grade_Userinfo, userID))
        self.cu.execute(sql)
        response = self.cu.fetchone()
        return {'username':response[0],
                'password':response[1],
                'verify':response[2]}

def Convert2JSON(one):
    json = {'courseName':str(one[0]),
            'courseType' : str(one[1]),
            'credit' : str(one[2]),
            'totalGrade' : str(one[3]),
            'finalGrade' : str(one[4]),
            'gradePoint' : str(one[5]),
            'updateTime' : str(one[6]),}
    return simplejson.dumps(json)
def Convert2Text(one):
    if (len(one) == 0):
        return None
    result = ''
    # result = 'courseName:'+str(one[0])+'\n'+ 'courseType:'+str(one[1])+'\n'+ 'credit:'+str(one[2])+'\n'+ 'totalGrade:'+str(one[3])+'\n'+ 'finalGrade:'+str(one[4])+'\n'+ 'gradePoint:'+str(one[5])+'\n'+ 'updateTime:'+str(one[6])+'\n'
    result = result + 'courseName:'+str(one[0])+'\n'
    result = result + 'courseType:'+str(one[1])+'\n'
    result = result + 'credit:'+str(one[2])+'\n'
    result = result + 'totalGrade:'+str(one[3])+'\n'
    result = result + 'finalGrade:'+str(one[4])+'\n'
    result = result + 'gradePoint:'+str(one[5])+'\n'
    result = result + 'updateTime:'+str(one[6])+'\n'
    return result


class API:
    def __init__(self, minutes, db = 'data.db'):
        self.db = db
        self.minutes = int(minutes)
        self.cx = sqlite3.connect(db)
        self.cu = self.cx.cursor()
        self.school_grades = 'school_grades'
        self.school_userinfo = 'school_userinfo'


    def checker(self, belongs_id=None, username=None):
        if belongs_id is None and username is None:
            sql = 'select id, belongs_id, username, password, cookies from %s;' % (self.school_userinfo)
        elif belongs_id is None:
            sql = 'select id, belongs_id, username, password, cookies from %s where username=\'%s\';' % (self.school_userinfo, username)
        elif username is None:
            sql = 'select id ,belongs_id, username, password, cookies from %s where belongs_id=\'%s\';' % (self.school_userinfo, belongs_id)
        else:
            sql = 'select id, belongs_id, username, password, cookies from %s where belongs_id=\'%s\' and username=\'%s\';' % (self.school_userinfo, belongs_id, username)
        self.cu.execute(sql)
        response = self.cu.fetchall()

        ans = []
        for i in response:
            new_grades = []
            new_grades = self.get_new(*i)
            if new_grades == False:
                _ = contact(self.db)
                mail = _.get_school_alert_mail(i[0])
                message = 'password and cookies error %s\n' % (i[2])
                ans.append({'email': mail, 'message': [message]})
            elif len(new_grades) != 0:
                _ = contact(self.db)
                mail = _.get_school_alert_mail(i[0])
                message = []
                for one in new_grades:
                    a_grade = '''
                    %s学年 第 %s 学期 %s 课程(%s, %s学分) 成绩更新\r\n
                    当前得分为 %s， 获得学分 %s， 最终得分 %s\r\n
                    检测时间 %s\r\n
                    \r\n
                    ''' % (one[2], one[3], one[6], one[7], one[8], one[9], one[12], one[11], one[13])
                    message.append(a_grade)
                ans.append({'email': mail, 'message': message})
            else:
                pass
        return ans




    def get_new(self, _id, belongs_id, username, password, cookies):
        _ = uestc(self.db)
        status = _.login(belongs_id, username, password, cookies)
        if status:
            li = []
            li = _.get_list_course()
            _.update_db(belongs_id, li)
            time_str = ((datetime.datetime.now() - datetime.timedelta(minutes = self.minutes)).strftime('%Y-%m-%d %H:%M:%S'))
            sql = "select * from %s where updateTime>'%s'" % (self.school_grades, time_str)
            self.cu.execute(sql)
            new_grades = self.cu.fetchall()
        else:
            new_grades = False

        return new_grades






if __name__ == '__main__':
    pass
