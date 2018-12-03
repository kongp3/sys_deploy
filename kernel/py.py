# -*- coding:utf-8 -*-
from fabric.colors import blue, red
from fabric.contrib.files import run, cd

from config import PY_SYS_DEPLOY_PATH, SUPERVISORD_CONF_DIR
from kernel import DeployBase
from toolkit.deploy_fuc import mk_deploy_log, supervisrord_restart, supervisrord_all, pip_requirement


class Py(DeployBase):
    def __init__(self, **kwargs):
        super(Py, self).__init__(**kwargs)
        self.sys_deploy_path = PY_SYS_DEPLOY_PATH

    def build_server_file(self):
        with cd(self.sys_deploy_path):
            run('tar -zxf ' + self.name + '.tar.gz', quiet=True)
            run('rm ' + self.name + '.tar.gz')

    def restart_job(self):
        if self.job_group is None:
            supervisrord_all(SUPERVISORD_CONF_DIR)
        else:
            supervisrord_restart(SUPERVISORD_CONF_DIR, self.job_group)

    def deploy(self):
        # 将文件发送到服务器
        print blue('将文件发送到服务器')
        self.send_to_server()

        # 删除除了.deploy之外的所有文件
        print blue('删除除了.deploy之外的所有文件')
        self.clean_server_file()

        # 解压到指定目录并创建所需目录
        print blue('解压到指定目录并创建所需目录')
        self.build_server_file()

        # 安装依赖
        print blue('安装公共的Python库')
        if pip_requirement(self.sys_deploy_path + self.name, self.env) is False:
            print red('部署中断.')
            return

        # 重启服务
        print blue('重启服务ing')
        self.restart_job()

        # 创建部署时间文件
        print blue('创建部署时间文件')
        mk_deploy_log(self.sys_deploy_path + self.name, self.branch)
