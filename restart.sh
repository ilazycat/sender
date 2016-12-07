#! /bin/sh

git pull
pkill uwsgi
ps -aux | grep uwsgi
systemctl restart nginx
