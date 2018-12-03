# -*- coding: utf-8 -*-

from fabric.colors import *

from application import local_operate, error_handler
from kernel.py import Py


@error_handler
@local_operate
def deploy_python(**kwargs):
    sys_name = kwargs.get('sys_name')
    git = kwargs.get('git')
    branch = kwargs.get('branch')
    env_dir = kwargs.get('env_dir')
    group = kwargs.get('group')

    name = kwargs.get('name')

    py = Py(git_path=git, name=name, branch=branch, env=env_dir, job_group=group)
    py.deploy()
    print green("%s部署完成" % sys_name)
