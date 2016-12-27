import sqlite3
import requests
import json
import datetime
from .get_contact_api import API as contact

class API:
    def __init__(self, db='data.db'):
        self.db = db
        self.cx = sqlite3.connect(db)
        self.cu = self.cx.cursor()
        self.table = 'kuaidi_kuaidiinfo'

    def get_all_nums(self):
        sql = ("select distinct num from %s;" % (self.table))
        self.cu.execute(sql)
        response = self.cu.fetchall()
        result = []
        for one in response:
            result.append(one[0])
        return result

    def get_id_nums(self, belongs_id):
        sql = ("select distinct num from %s where belongs_id=%d;" % (self.table, belongs_id))
        self.cu.execute(sql)
        response = self.cu.fetchall()
        result = []
        for one in response:
            result.append(one[0])
        return result

    def get_belongs_id_by_num(self, num):
        sql = ("select distinct belongs_id from %s where num='%s';" % (self.table, num))
        self.cu.execute(sql)
        response = self.cu.fetchall()
        result = []
        for one in response:
            result.append(one[0])
        return result

    def fetch(self, num):
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
        request = requests.get(getExpressURL)
        result = json.loads(request.text)
        try:
            expressType = result['auto'][0]['comCode']
            ans['company'] = expressType
        except:
            ans['verify'] = -1
            ans['message'] = 'bad input, can not find company or no this code'
            return ans
        getLogisticsURL  = ('http://www.kuaidi100.com/query?type=%s&postid=%s' % (expressType, trackingNumber))
        request = requests.get(getLogisticsURL)
        result = json.loads(request.text)
        ans['message'] = result['message']
        try:
            ans['data'] = result['data']
            ans['updateTime'] = result['data'][0]['ftime']
            ans['verify'] = 1
        except:
            ans['verify'] = 0   # find company, no data
            ans['updateTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return ans

    def query(self, num):
        sql = ("select company, comment, updateTime, belongs_id, submit from %s where num='%s';" % (self.table, num))
        self.cu.execute(sql)
        response = self.cu.fetchall()
        return response

    def add_new_router(self, num, company, comment, updateTime, time, context, belongs_id, submit):
        sql = 'insert into %s (num, company, comment, updateTime, time, context, belongs_id, submit) values("%s", "%s", "%s", "%s", "%s", "%s", "%d", "%s")' % (self.table, num, company, comment, updateTime, time, context, belongs_id, submit)
        self.cu.execute(sql)
        self.cx.commit()

    def update_time_fallback(self, num, updateTime):
        sql = 'update %s set updateTime="%s" where num="%s"' % (self.table, updateTime, num)
        self.cu.execute(sql)
        self.cx.commit()

    def update_by_num(self, num):
        latest = self.fetch(num)
        current = self.query(num)
        if current is []:
            return None
        elif current is None:
            return None
        elif latest['verify'] == 0:
            return None
        else:
            ans = {}
            company = current[0][0]
            comment = current[0][1]
            current_update = current[0][2]
            if current_update is None:
                current_update = ''
            belongs_id = current[0][3]
            submit = current[0][4]
            latest['data'].sort(key=lambda x:x['time'])
            for i in latest['data']:
                if i['time'] > current_update:
                    self.add_new_router(num, company, comment, i['time'], i['time'], i['context'], belongs_id, submit)
                    ans.update({num: {'time': i['time'], 'comment': comment, 'company': company, 'context': i['context']}})
            self.update_time_fallback(num, latest['updateTime'], )
        return ans

    def update_all(self):
        ans = []
        for num in self.get_all_nums():
            result = self.update_by_num(num)
            if result != {}:
                ans.append(result)
        return ans

    def rebuild_time(self, num, belongs_id):
        sql = 'select max(time) from %s where num=\'%s\' and belongs_id=%d' % (self.table, num, belongs_id)
        self.cu.execute(sql)
        try:
            update_time = self.cu.fetchall()[0][0]
            sql = 'update %s set updateTime="%s" where num="%s" and belongs_id=%d' % (self.table, update_time, num, belongs_id)
            self.cu.execute(sql)
            self.cx.commit()
        except IndexError:
            print('no num %s' % (num))


    def update_id(self, belongs_id):
        ans = []
        for num in self.get_id_nums(belongs_id):
            result = self.update_by_num(num)
            if result != {}:
                ans.append(result)
        return ans


    def check(self):
        nums = self.get_all_nums()

        print(nums)
        ans = []
        get_mail = contact(self.db)
        for i in nums:
            new_router = self.update_by_num(i)
            print(new_router)
            if new_router is None:
                continue
            elif len(new_router) == 0:
                continue
            else:
                for _id in self.get_belongs_id_by_num(i):
                    mail = get_mail.get_main_email_by_id(_id)
                    message = '''
                    [%s] 单号为[%s]的%s快递更新路由，\n
                    %s\n
                    更新时间 %s\n\n
                    ''' % (new_router[i]['comment'], i, new_router[i]['company'], new_router[i]['context'], new_router[i]['time'])
                    print(message)
                    ans.append({'email': mail, 'message': message})
        return ans

    def clean(self, days=7):
        submit_time = datetime.datetime.now() - datetime.timedelta(days=days)
        sql = 'delete from %s where submit < \'%s\';' % (self.table, submit_time.strftime('%Y-%m-%d'))
        print(sql)
        self.cu.execute(sql)
        self.cx.commit()

if __name__ == '__main__':
    pass
