import sqlite3
from SendMail_API import SendMail
from Uestc import Exec
from Uestc2db import DB_uestc
import datetime
import re
import time
import simplejson
class DB:
    def __init__(self, db = 'data.db'):
        self.cx = sqlite3.connect(db)
        self.cu = self.cx.cursor()
        self.Grade_Grades = 'grade_grades'
        self.Grade_Userinfo = 'grade_userinfo'
    def getNewUestc(self, minutes = 10):
        timeStr = ((datetime.datetime.now() - datetime.timedelta(minutes = minutes)).strftime('%Y-%m-%d %H:%M:%S'))
        sql = ("select * from %s where updateTime>'%s'" % (self.Grade_Grades, timeStr))
        self.cu.execute(sql)
        # print (sql)
        return self.cu.fetchall()
    def getNewUestcByID(self, belongs_id = 0, minutes = 10):
        timeStr = ((datetime.datetime.now() - datetime.timedelta(minutes = minutes)).strftime('%Y-%m-%d %H:%M:%S'))
        sql = ("select courseName,courseType,credit,totalGrade,finalGrade,gradePoint,updateTime from %s where belongs_id='%s' and updateTime>'%s'" % (self.Grade_Grades, belongs_id, timeStr))
        self.cu.execute(sql)

        response = self.cu.fetchall()
        result = []
        for one in response:
            # print (one)
            # result.append(Convert2JSON(one))
            result.append(Convert2Text(one))
        return '-----------\n'.join(result)
    def getEmail(self, userID):
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
        # print (response)
        # return re.split(',| ', response[0])
    def getUsernameAndPasswordByID(self, userID):
        sql = ("select username,password,verify from %s where id=%d" % (self.Grade_Userinfo, userID))
        #TODO: HERE

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

if __name__ == '__main__':
    while(True):
        # main()
        pass
def Sender():
    db = DB('../../data.db')
    user = db.getUsersBySchool('uestc')
    for one in user:
        email = db.getEmail(one)
        content = db.getNewUestcByID(one,100000)

        if (len(content) > 0):
            SendMail('Grades', content, email)

def Checker():
    user = userinfo.objects.filter(id = userinfoID)[0]
    li = Exec(user.username, user.password, 'courseList')
    db = DB_uestc(userinfoID)
    db.sync(li)
