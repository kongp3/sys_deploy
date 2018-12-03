# -*- coding: utf-8 -*-
from fabric.colors import yellow
from fabric.contrib.files import local, put, run, exists, cd

from config import MASTER_TMP
from toolkit.deploy_fuc import rm_useless_file, rm_all_except


class DeployBase(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.branch = kwargs.get('branch')
        self.job_group = kwargs.get('job_group')
        self.env = kwargs.get('env')
        self.master_tmp = MASTER_TMP

        self.sys_deploy_path = ''

    def send_to_server(self):
        print yellow('如果服务器在香港,请耐心等待...')
        local('tar -zcf ' + self.master_tmp + self.name + '.tar.gz -C ' + self.master_tmp + ' ' + self.name)
        put(self.master_tmp + self.name + '.tar.gz', self.sys_deploy_path, use_sudo=True)

    def clean_server_file(self):
        if exists(self.sys_deploy_path + self.name) is False:
            run('mkdir ' + self.sys_deploy_path + self.name)
        else:
            rm_useless_file(self.sys_deploy_path + self.name)
            with cd(self.sys_deploy_path + self.name):
                rm_all_except()
