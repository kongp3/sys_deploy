# -*- coding:utf-8 -*-
from fabric.contrib.files import *

from config import BRANCH, DEPLOY_FLAG
from config.git_path import TE_GIT
from config.hosts import SERVER_HOSTS

from application.inner_web import deploy_web
from application.py import deploy_python

''' web_sys '''


@task(name='php_sys')
@hosts(SERVER_HOSTS)
def apps_customer_web(branch=BRANCH):
    deploy_web(
        sys_name='【XX产品】php_sys',
        git=TE_GIT['php_sys'],
        branch=branch,
        deploy_flag=DEPLOY_FLAG
    )


'''PYTHON 系统'''


@task(name='py_sys')
@hosts(SERVER_HOSTS)
def apps_tcore(branch=BRANCH):
    deploy_python(
        sys_name='【XX产品】py_sys',
        git=TE_GIT['php_sys'],
        branch=branch,
        # env_dir='',
        deploy_flag=DEPLOY_FLAG
    )
