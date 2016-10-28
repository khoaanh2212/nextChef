# -*- coding: utf-8 -*-
"""
Fabric tasks for Altruistip project.
"""
from os import environ
from datetime import datetime
from fabric.api import env, run, sudo, cd


# Aws credentials
AWS_PRIVATE_KEY_FILE = "~/.aws/cbit.pem"
AWS_EC2_USERNAME = "admin"
AWS_REGION = 'eu-west-1'
AWS_MASTER_INSTANCE = 'ec2-54-75-232-203.eu-west-1.compute.amazonaws.com'
AWS_STAGING_INSTANCE = 'ec2-54-74-126-235.eu-west-1.compute.amazonaws.com'

# Fabric environment variables
env.key_filename = AWS_PRIVATE_KEY_FILE
env.user = AWS_EC2_USERNAME

# Project related settings
ARCHIVE_PATH = '/home/' + AWS_EC2_USERNAME + '/deploy_backups'
PROJECT_PATH = '/home/' + AWS_EC2_USERNAME + '/sites/backend'
DJANGO_PATH = PROJECT_PATH
WORKON_CMD = 'workon cookbooth'


#
# Tasks
#
def master():
    env.hosts = ['%s@%s' % (AWS_EC2_USERNAME, AWS_MASTER_INSTANCE)]


def pre():
    env.hosts = ['%s@%s' % (AWS_EC2_USERNAME, AWS_STAGING_INSTANCE)]


def uptime():
    run("uptime")


def apt_update():
    sudo("apt-get update")


def clear_sessions():
    with cd(DJANGO_PATH):
        run('%s && ./manage.py clearsessions' % WORKON_CMD)


def staticfiles():
    with cd(DJANGO_PATH):
        run('%s && ./manage.py collectstatic --noinput' % WORKON_CMD)


def migrate():
    with cd(DJANGO_PATH):
        run('%s && ./manage.py migrate' % WORKON_CMD)


def update_trans():
    with cd(DJANGO_PATH):
        run('%s && ./manage.py compilemessages -l es' % WORKON_CMD)


def restart_apache():
    sudo('service apache2 restart')


def git_pull():
    with cd(PROJECT_PATH):
        run('git pull origin master')


def requirements():
    with cd(PROJECT_PATH):
        run('%s && pip install -r ../requirements/production.txt' % WORKON_CMD)


def archive():
    now = datetime.now()
    archive_name = "cookbooth-%s.tar.gz" % now.strftime("%Y%m%d%H%M")
    with cd(ARCHIVE_PATH):
        run('tar czvf %s %s' % (archive_name, PROJECT_PATH,))


def deploy():
    # archive()
    git_pull()
    requirements()
    # update_trans()
    staticfiles()
    restart_apache()
