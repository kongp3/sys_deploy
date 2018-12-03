# -*- coding:utf-8 -*-
from fabric.colors import magenta
from fabric.contrib.files import run, cd

from config import WEB_SYS_DEPLOY_PATH
from kernel import DeployBase
from toolkit.deploy_fuc import mk_deploy_log
from toolkit.deploy_cmd import t_mkdir, t_chmod


class InnerWeb(DeployBase):
    def __init__(self, **kwargs):
        super(InnerWeb, self).__init__(**kwargs)
        self.sys_deploy_path = WEB_SYS_DEPLOY_PATH

    def build_server_file(self):
        with cd(self.sys_deploy_path):
            run('tar -zxf ' + self.name + '.tar.gz', quiet=True)
            run('rm ' + self.name + '.tar.gz')
        t_mkdir(self.sys_deploy_path + self.name + '/logs')
        t_mkdir(self.sys_deploy_path + self.name + '/tmp')
        t_chmod(self.sys_deploy_path + self.name + '/logs', '777', '-R')
        t_chmod(self.sys_deploy_path + self.name + '/tmp', '777', '-R')

    def deploy(self):
        # 将文件发送到服务器
        print magenta('将文件发送到服务器')
        self.send_to_server()

        # 删除除了.deploy之外的所有文件
        print magenta('删除除了.deploy之外的所有文件')
        self.clean_server_file()

        # 解压到指定目录并创建所需目录
        print magenta('解压到指定目录并创建所需目录')
        self.build_server_file()

        # 创建部署时间文件
        print magenta('创建部署时间文件')
        mk_deploy_log(self.sys_deploy_path + self.name, self.branch)
