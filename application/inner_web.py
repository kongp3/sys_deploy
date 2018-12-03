# -*- coding: utf-8 -*-

from fabric.colors import *

from application import local_operate, error_handler
from kernel.inner_web import InnerWeb


@error_handler
@local_operate
def deploy_web(**kwargs):

    sys_name = kwargs.get('sys_name')
    git = kwargs.get('git')
    branch = kwargs.get('branch')

    name = kwargs.get('name')

    web = InnerWeb(git_path=git, name=name, branch=branch)
    web.deploy()
    print green("%s部署完成" % sys_name)
