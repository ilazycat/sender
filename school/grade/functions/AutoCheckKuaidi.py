import sqlite3
from SendMail_API import SendMail
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
        self.table = 'grade_kuaidiinfo'
    def refresh(self):
        pass
    def getNum(self):
        # return list of all nums
        sql = ("select distinct num from %s;" % (self.table))
        self.cu.execute(sql)
        response = self.cu.fetchall()
        result = []
        for one in response:
            result.append(one[0])
        return result
    def getNumById(self, belongs_id):
        # return list of all nums
        sql = ("select distinct num from %s where belongs_id=%d;" % (self.table, belongs_id))
        self.cu.execute(sql)
        response = self.cu.fetchall()
        result = []
        for one in response:
            result.append(one[0])
        return result
    def queryKuaidi(self,num):
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
            ans['updateTime'] = result['data'][0]['time']
            ans['verify'] = 1
        except:
            ans['verify'] = 0   # find company, no data
        return ans

    def updateByNum(self, num, latest):
        print ('update!')
        ans = ''
        # add not exists
        company = latest['company']
        # latest = {'updateTime':'2016-03-02 22:22:22', 'data':[{'time':'2016-03-02 22:22:22','context':'1'}, {'time':'2016-03-01 22:00:00','context':'2'}, {'time':'2016-03-01 21:41:48','context':'3'}, {'time':'2016-03-01 18:05:00','context':'4'}]}
        # db = '/home/lc4t/Documents/git/sender/school/data.db'
        # cx = sqlite3.connect(db)
        # cu = cx.cursor()
        # table = 'grade_kuaidiinfo'
        sql = ("select distinct updatetime from %s where num='%s'" % (self.table, num))
        self.cu.execute(sql)
        response = self.cu.fetchall()
        if (len(response) != 1):
            print (response)
            print ('error')
            return ans
        oldTime = response[0][0]
        # ans = latest['data'][-1]
        for i in range(len(latest['data']) - 1, 0 - 1, -1):
            newData = latest['data'][i]
            if (newData['time'] > oldTime):
                sql = ("insert into %s (belongs_id, num, company, time, context, comment) values ((select (select distinct belongs_id from %s where num='%s')), '%s', '%s', '%s', '%s', (select (select distinct comment from %s where num='%s')));" % (self.table, self.table, num, num, company, newData['time'], newData['context'], self.table, num, ))
                self.cu.execute(sql)
                self.cx.commit()
        sql = ("update %s set updatetime='%s'  where num='%s'" % (self.table, latest['updateTime'], num))
        self.cu.execute(sql)
        self.cx.commit()

        sql = ("select context from %s where num='%s' and time='%s';" % (self.table, num, latest['updateTime']))
        self.cu.execute(sql)
        ans = self.cu.fetchall()[0][0]
        ans = {'time':latest['updateTime'], 'context':ans}
        return ans
    def getCommentById(self, num):
        sql = ("select distinct comment from %s where num='%s'" % (self.table, num))
        self.cu.execute(sql)
        comment = self.cu.fetchall()[0][0]
        return comment
    def getBelongsById(self, num):
        sql = ("select distinct belongs_id from %s where num='%s'" % (self.table, num))
        self.cu.execute(sql)
        belongs_id = self.cu.fetchall()[0][0]
        return belongs_id
    def checkUpdate(self, num):
        queryAns = self.queryKuaidi(num)
        if (queryAns['verify'] > 0):
            latest = queryAns
            # start check
            sql = ("select updatetime from %s where num='%s' and updatetime='%s';" % (self.table, num, latest['updateTime']))
            self.cu.execute(sql)
            response = self.cu.fetchall()
            if (len(response) == 0):# no match, but now have updateTime new!
                ans = self.updateByNum(num, latest)
                comment = self.getCommentById(num)
                return [comment, num, ans['time'], ans['context']]
            else:
                print ('no update')
                return []
            # check end
        else:
            print ('verify error in checkUpdate')
    def getUserEmailById(self, num):
        userID = self.getBelongsById(num)
        sql = ("select email from %s where id=%d" % ('auth_user', int(userID)))
        self.cu.execute(sql)
        response = self.cu.fetchone()
        return re.split(',| ', response[0]) # list
    

class Refresh:
    def __init__(self, belongs_id):
        self.belongs_id = belongs_id
        self.Run()

    def Run(self):
        db = DB('data.db')
        nums = db.getNumById(int(self.belongs_id))
        count = 0
        for num in nums:
            if (len(db.checkUpdate(num)) > 0):
                count += 1
        return count
                

def Sender(minutes = 3, database = '../../data.db', mode = 'email'):
    db = DB(database)
    while (True):
        nums = db.getNum()
        for num in nums:
            print ('check', num)
            try:

                content = db.checkUpdate(num)
                content =  '快递:' + content[0] + '\n' + '单号:' + content[1] + '\n' + '更新时间:' + content[2] + '\n' + '动态:' + content[3] + '\n'
                email = db.getUserEmailById(num)


                if (mode == 'email'):
                    print (content)
                    print ('send to '+','.join(email) + ' -->' +  ' @ ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    SendMail('Kuaidi', content, email)
            except Exception as e:
                print ('-------ERROR-------')
                print (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                print (num)
                print (e)
                print ('-------_END_-------')

        if (mode == 'email'):
            print ('sleep @ '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            time.sleep(minutes * 60)
        



if __name__ == '__main__':
    usage = "usage: %prog [options] arg"
    parser = OptionParser()
    parser.add_option('-f', '--function', help = 'run for refresh or monitor')
    parser.add_option('-t', '--time', help = 'Time for onetime')
    # parser.add_option('-w', '--way', help = '1.: shell.  2.crontab.')
    (options, args) = parser.parse_args()
    if (options.function == 'refresh'):
        Sender(mode = 'refresh')
    elif (options.function == 'monitor' and options.time != ''):
        Sender(minutes = int(options.time), mode = 'email')
    else:
        parser.print_help()
        exit(0)
