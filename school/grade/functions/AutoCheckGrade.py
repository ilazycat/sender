import sqlite3
from SendMail_API import SendMail
from Uestc import Exec
from Uestc2db import DB_uestc
import datetime
import re
import time
import threading
import simplejson
from optparse import OptionParser
class DB:
    def __init__(self, db = '../../data.db'):
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
            # print (one)
            # result.append(Convert2JSON(one))
            result.append(Convert2Text(one))
        print ('-----------\n'.join(result))
        return '-----------\n'.join(result)
    # def getNewUestcByID(self, belongs_id = 0, minutes = 10):
    #     timeStr = ((datetime.datetime.now() - datetime.timedelta(minutes = minutes)).strftime('%Y-%m-%d %H:%M:%S'))
    #     sql = ("select courseName,courseType,credit,totalGrade,finalGrade,gradePoint,updateTime from %s where belongs_id='%s' and updateTime>'%s'" % (self.Grade_Grades, belongs_id, timeStr))
    #     self.cu.execute(sql)

    #     response = self.cu.fetchall()

    #     result = []
    #     for one in response:
    #         # print (one)
    #         # result.append(Convert2JSON(one))
    #         result.append(Convert2Text(one))
    #     print ('-----------\n'.join(result))
    #     return '-----------\n'.join(result)
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
        # print (response)
        # return re.split(',| ', response[0])
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


def Sender(school = 'uestc', minutes = 10, database = '../../data.db'):
    db = DB(database)
    users = db.getUsersBySchool(school)
    # while(True):
    for userID in users:   # users: all user from uestc list, @ userInfo-->
        userInfo = db.getUsernameAndPasswordByID(userID)
        if (userInfo['verify'] == True):
            try:
                li = Exec(userInfo['username'], userInfo['password'], 'courseList')
                if (li == 'Authentication failed'):
                    cx = sqlite3.connect(database)
                    cu = cx.cursor()
                    sql = ("update grade_userinfo set verify=0  where school='%s' and username='%s';" % ('uestc', username))
                    cu.execute(sql)
                    cx.commit()
                    continue
                # print (li)
                DB_uestc(userID, database).sync(li)
                email = db.getEmailByID(userID)
                content = db.getNewUestcByID(userID, minutes)
                # print (content)
                # print (len(content))
                # exit(0)

                if (len(content) > 0):
                    print (content)
                    print ('send to '+','.join(email) + ' -->' + userInfo['username'] + ' @ ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    SendMail('Grades', content, email)
                else:
                    print ('No update for ' + userInfo['username'] + ' @ ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            except Exception as e:
                print ('-------ERROR-------')
                print (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                print ('school:' + school + ' username:' + userInfo['username'] + ' verify:' + str(userInfo['verify']))
                print (e)
                print ('-------_END_-------')
        # print ('sleep @ '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # time.sleep(minutes * 60)



if __name__ == '__main__':
    usage = "usage: %prog [options] arg"
    parser = OptionParser()
    parser.add_option('-s', '--school', help = 'Your school')
    parser.add_option('-t', '--time', help = 'Time for onetime')
    parser.add_option('-w', '--way', help = '1.: shell.  2.crontab.')
    (options, args) = parser.parse_args()
    if (options.school == None or options.time == None or options.way == None):
        parser.print_help()
        exit(0)
    if (options.way == 'shell'):
        while(True):
            Sender(options.school, int(options.time))
            print ('sleep @ '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            time.sleep(int(options.time) * 60)
    elif (options.way == 'crontab'):
        Sender(options.school, int(options.time))
        print ('done @ '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        parser.print_help()
    exit(0)

    # Sender('uestc',10)
    # threads = []
    # t1 = threading.Thread(target = Sender, args = ('uestc', 1))
    # threads.append(t1)
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    # while (1):
    #     continue
    
