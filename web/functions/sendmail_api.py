import smtplib
from email.mime.text import MIMEText


class API:
    def __init__(self, host, user, passwd, postfix = None):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.postfix = user[user.rfind('@')+1:]if postfix is None else postfix

    def send(self, subject, content, to = []):
        me = self.user
        msg = MIMEText(content, _subtype='html', _charset='utf-8')
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = ';'.join(to)
        server = smtplib.SMTP()
        server.connect(self.host)
        server.login(self.user, self.passwd)
        server.sendmail(me, to, msg.as_string())
        server.close()
        return True
