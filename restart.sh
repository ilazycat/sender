#! /bin/sh

git pull
pkill uwsgi
ps -aux | grep uwsgi
uwsgi --ini=uwsgi.ini
systemctl restart nginx
