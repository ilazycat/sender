from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task
from .sendmail_api import API as sendmail
from .kuaidi_api import API as kuaidi
from .get_contact_api import API as get_email
from .school_uestc_grade_check_api import API as uestc_check_grade


@periodic_task(run_every=crontab(minute='*/5'), name='check_kuaidi')
def check_kuaidi():
    _ = kuaidi()
    ans = _.check()
    if len(ans) == 0:
        print('no update kuaidi')
        return
    else:
        for i in ans:
            send_mail.delay('快递更新', i['message'], i['email'])

@shared_task(default_retry_delay=5, max_retries=3, name='send_mail')
def send_mail(subject, content, to):
    'to: []'
    print('sender ready: %s %s\r\n%s' % (str(to), subject, content))
    content = content.replace('\n', '<br/>')
    sender = sendmail('smtp.ym.163.com', 'robot@lc4t.me', '')
    sender.send(subject, content, to)


@shared_task(name='get_main_email')
def get_main_email(user_id):
    _ = get_email().get_main_email_by_id(user_id)
    return list(_)


@shared_task(name='get_school_alert_email')
def get_school_alert_email(belongs_id):
    _ = get_email().get_school_alert_mail(belongs_id)
    return _


@periodic_task(run_every=crontab(minute='*/30'), name='uestc_send_grade')
def uestc_send_grade():
    _ = uestc_check_grade(30)
    ans = _.checker()
    if len(ans) == 0:
        print('No update uestc grade')
        return
    else:
        for i in ans:
            send_mail.delay('成绩通知', '\r\n'.join(i['message']), i['email'])
