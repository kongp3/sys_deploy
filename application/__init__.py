# -*- coding: utf-8 -*-
import os

from functools import wraps

from fabric.colors import *

from config import MASTER_TMP
from toolkit.deploy_fuc import warning_for_env, git_init, clean_local_file, yaml2dict, set_config_file


def error_handler(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print red(e.message)
        finally:
            clean_local_file()

    return decorated_function


def local_operate(f):
    """
    处理数据库异常和返回错误信息
    :param f:
    :return:
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        sys_name = kwargs.get('sys_name')
        git = kwargs.get('git')
        branch = kwargs.get('branch')
        deploy_flag = kwargs.get('deploy_flag')

        result = warning_for_env(sys_name, branch, deploy_flag)
        if result is False:
            raise Exception('停止部署: 用户选择取消')

        print green("%s部署开始" % sys_name)
        name = git.split('/')[-1].split('.')[0]
        clean_local_file()
        git_init(git, MASTER_TMP, name, branch)
        deploy_yaml = yaml2dict(MASTER_TMP + name + '/deploy.yaml')  # 读取工程根目录下的yaml文件 获取replace_list

        if deploy_yaml is False:
            raise Exception('停止部署: 文件缺失,请在您的工程根目录添加deploy.yaml!')

        if deploy_yaml.get('config') is None:
            raise Exception('停止部署: 您的deploy.yaml文件内容有误, 请检查!')

        replace_list = deploy_yaml.get('config')
        if deploy_yaml.get('supervisord'):
            group = deploy_yaml['supervisord']['group']
            kwargs['group'] = group

        if deploy_yaml.get('env'):
            env_dir = deploy_yaml['env']['dir']
            kwargs['env_dir'] = env_dir

        for value in replace_list:
            file_path = MASTER_TMP + value
            if os.path.exists(file_path) is False:
                raise Exception('停止部署: deploy.yaml中的config路径错误, 请仔细阅读文档后重新配置! '
                                'http://10.180.55.111:8088/x/x-mind/issues/15')

        if set_config_file(replace_list) is False:
            raise Exception('停止部署: 用户检查配置文件时发现问题!')
        kwargs['name'] = name

        return f(*args, **kwargs)

    return decorated_function
