# -*- coding:utf-8 -*-
from fabric.colors import magenta
from fabric.contrib.files import run, cd, sudo

from config import WEB_SYS_DEPLOY_PATH
from kernel import DeployBase
from toolkit.deploy_fuc import mk_deploy_log, rm_all_except
from toolkit.deploy_cmd import t_mkdir, t_chmod


class SaasWeb(DeployBase):
    def __init__(self, **kwargs):
        super(SaasWeb, self).__init__(**kwargs)
        self.sys_deploy_path = WEB_SYS_DEPLOY_PATH

    def build_server_file(self):
        with cd(self.sys_deploy_path):
            rm_all_except()
            # 5.4 解压
            sudo('tar -zxf ' + self.name + '.tar.gz --strip-components 1', quiet=True)  # 解压完了是web下面的东西
            sudo('rm ' + self.name + '.tar.gz')
        t_mkdir(self.sys_deploy_path + 'logs')
        t_mkdir(self.sys_deploy_path + 'tmp')
        t_chmod(self.sys_deploy_path + 'logs', '777', '-R')
        t_chmod(self.sys_deploy_path + 'tmp', '777', '-R')

    def deploy(self):

        # 将文件发送到服务器
        print magenta('将文件发送到服务器')
        self.send_to_server()

        print magenta('解压到指定目录并创建所需目录')
        self.build_server_file()
        print magenta('创建部署时间文件')
        mk_deploy_log(self.sys_deploy_path, self.branch)
