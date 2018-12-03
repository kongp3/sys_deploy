# -*- coding:utf-8 -*-
import yaml
import socket
import arrow

from fabric.contrib.files import *
from fabric.colors import *

from config import *
from config.auth_info import auth_info

from contextlib import contextmanager as _contextmanager

# local


def modify_config(mod_file_name):
    # 1. 按原配置文件的名字 + .new 生成新的文件
    new_file = open(mod_file_name + '.new', 'w')
    # 2. 打开原配置文件读取内容
    mod_file = open(mod_file_name, 'r')
    for line in mod_file:
        for key in auth_info:
            line = line.replace(key, auth_info[key])
        new_file.write(line)
    # 3. 关闭两个文件
    new_file.close()
    mod_file.close()
    # 4. 把新生成的配置文件按原来的名字覆盖原始配置文件
    local('mv ' + mod_file_name + '.new' + ' ' + mod_file_name)


def t_git_get(git_path, local_tmp_path):
    try:
        with lcd(local_tmp_path):
            local("git clone " + git_path)
    except Exception, e:
        print e


def git_init(git_path, master_tmp, sys_path, branch=None):
    t_git_get(git_path, master_tmp)
    # 切换分支再清理
    with lcd(master_tmp + sys_path):
        if branch is not None:
            local('git checkout ' + branch)
        local('git pull')
    rm_useless_file(master_tmp + sys_path, 'local')


def clean_local_file():
    print green('删本地临时文件')
    with settings(warn_only=True):
        local('rm -rf ' + MASTER_TMP + '*')


def warning_for_env(sys_name, branch, deploy_flag):
    env_str = ''
    if deploy_flag == 'prod':
        env_str = '生产环境'
    elif deploy_flag == 'test':
        env_str = '测试环境'
    if branch is None:
        branch = 'master'
    else:
        branch = branch
    result = prompt(green('您正在') + red(env_str) + green('部署') + yellow(sys_name) + green('系统') \
                    + red(',分支' + branch) + green(',是否继续?'), default='y/n')

    if str(result) == 'y' or str(result) == 'Y':
        return True
    else:
        return False


def pause_to_check():
    result = prompt(green('\n请检查您的配置文件是否正确?'), default='配置正确我要继续(y)/配置不正确通知部署脚本开发者(n)')
    if str(result) == 'y' or str(result) == 'Y':
        return True
    else:
        return False


def rm_useless_file(sys_dir, op_type='remote'):
    tmp_file_list = [
        '/.DS_Store',
        '/.git',
        '/.gitignore'
    ]
    for tmp_file in tmp_file_list:
        if op_type == 'remote':
            if exists(sys_dir + tmp_file):
                run('rm -rf ' + sys_dir + tmp_file)
        else:
            if os.path.exists(sys_dir + tmp_file):
                local('rm -rf ' + sys_dir + tmp_file)


# remote


def supervisrord_restart(conf_dir, group):
    with cd(conf_dir):
        run('supervisorctl -c supervisord.conf -u {uname} -p {pswd} restart {group}:'.format(uname=SUPERVISORD_USER,
                                                                                             pswd=SUPERVISORD_PASS,
                                                                                             group=group))


def supervisrord_all(conf_dir):
    with cd(conf_dir):
        run('supervisorctl -c supervisord.conf -u {uname} -p {pswd} restart all'.format(uname=SUPERVISORD_USER,
                                                                                        pswd=SUPERVISORD_PASS
                                                                                        ))


def rm_all_except():
    sudo('ls -a |  grep -v *.tar.gz | '
         'grep -v ENV | '
         'grep -v venv | '
         'grep -v .code_deploy | '
         'grep -v log | '
         'grep -v logs | '
         'grep -v tmp | '
         'sudo xargs rm -rf',
         warn_only=True)
    run('ls -l -a ')


def time_str():
    utc = arrow.utcnow()
    local_area = utc.to('Asia/Shanghai')
    return local_area.format('YYYY-MM-DD-HH:mm:ss')


def mk_deploy_log(sys_dir, branch):
    if '/' in branch:
        branch = branch.replace('/', '-')
    my_name = socket.getfqdn(socket.gethostname())
    with cd(sys_dir):
        if exists('.deploy_log') is False:
            sudo('mkdir .deploy_log')
        sudo('touch .deploy_log/' + time_str() + '-' + branch + '-' + my_name)


@_contextmanager
def virtualenv(sys_dir, env_dir):
    directory = sys_dir + '/' + env_dir
    activate = 'source ' + directory + '/bin/activate'
    with cd(directory):
        with prefix(activate):
            yield


def pip_requirement(sys_dir, env_dir):
    if env_dir == '':
        return True
    if exists(sys_dir + '/' + env_dir) is False:
        run('virtualenv ' + sys_dir + '/' + env_dir)
        with cd(sys_dir + '/' + env_dir + '/lib/python2.7/site-packages'):
            run('ln -s /home/admin/tcore .')

    with virtualenv(sys_dir, env_dir):
        if exists(sys_dir + '/requirements.txt') is False:
            print sys_dir + '/requirements.txt'
            print red('您的Python项目根目录下缺少requirements.txt文件, 请补齐上传后,重新执行部署!!!!')
            return False
        run('pip install --upgrade pip', warn_only=True)
        run('pip install -r ' + sys_dir + '/requirements.txt', warn_only=True)
        run('deactivate')
    return True

    # http://stackoverflow.com/questions/1180411/activate-a-virtualenv-via-fabric-as-deploy-user


def yaml2dict(y_file):
    import os
    if os.path.exists(y_file) is False:
        return False
    with open(y_file, 'r') as y:
        d = yaml.load(y)
        print d
        return d


def set_config_file(replace_list):
    # import os
    for value in replace_list:
        file_path = MASTER_TMP + value
        # if os.path.exists(file_path) is False:
        #     print red('部署中断.')
        #     return False
        modify_config(file_path)
        local('ccat ' + file_path)
        # 停下来检查配置文件
        if pause_to_check() is False:
            print red('部署中断.')
            return False
    return True


# if __name__ == '__main__':
#     yaml2dict('/Users/kongfm/PycharmProjects/code_deploy/code_deploy/toolkit/code_deploy.yaml')
