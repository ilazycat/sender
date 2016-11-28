from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task
from .sendmail_api import API as sendmail
from .kuaidi_api import API as kuaidi
from .get_contact_api import API as get_email

@periodic_task(run_every=crontab(minute=10), name='test')
def test():
    print(1)

@periodic_task(run_every=crontab(minute=1), name='check_kuaidi')
def check_kuaidi():
    # api = kuaidi().update_id(1)
    pass


@shared_task(name='send_mail')
def send_mail(subject, content, to):
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
