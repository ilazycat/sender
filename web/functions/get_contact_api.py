import sqlite3

class API:
    def __init__(self, db = 'data.db'):
        self.cx = sqlite3.connect(db)
        self.cu = self.cx.cursor()

    def get_main_email_by_id(self, belongs_id):
        # get regist auth email
        sql = 'select email from %s where id=%d' % ('auth_user', belongs_id)
        self.cu.execute(sql)
        response = self.cu.fetchall()
        result = []
        for one in response:
            result.append(one[0])
        return result

    def get_school_alert_mail(self, _id):
        # get school alert email in userinfo
        sql = 'select email from %s where id=%d' % ('school_userinfo', _id)
        self.cu.execute(sql)
        response = self.cu.fetchall()
        result = []
        for one in response:
            result = result + one[0].split(',')
        return result


if __name__ == '__main__':
    a = API().get_main_email_by_id(1)
    print(a)
    # print(a.get_main_email_by_id(1))
    # list_email = a.get_school_alert_mail(1)
