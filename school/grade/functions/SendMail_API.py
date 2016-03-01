import smtplib
from email.mime.text import MIMEText
import datetime
class SendMail:
    #5YceTh1Nxf
    def __init__(self,sub = 'sub', content = 'content', mailTo = ['lpylzx1@qq.com'], mailHost = 'smtp.ym.163.com',mailUser = 'robot@lc4t.me', mailPassword = '', mailPosfix = 'lc4t.me'):

        self.sub = sub # subject
        self.content = content
        self.mailTo = mailTo
        self.mailHost = mailHost  # server
        self.mailUser = mailUser    # username
        self.mailPass = mailPassword  # password
        self.mailPostfix = mailPosfix  # posfix


        if self.sendMail(self.mailTo, self.sub, self.content):
            print ('send success @ ' + ','.join(mailTo) + ' ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            print ('send faild ' + ','.join(mailTo) +' ' +datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


    def sendMail(self,to_list, sub, content):
        me="lc4t"+"<"+self.mailUser+"@"+self.mailPostfix+">"
        msg = MIMEText(content,_subtype='plain',_charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            server = smtplib.SMTP()
            server.connect(self.mailHost)
            server.login(self.mailUser,self.mailPass)
            server.sendmail(me, to_list, msg.as_string())
            # print (to_list)
            server.close()
            return True
        except Exception as e:
            print (str(e))
            return False
