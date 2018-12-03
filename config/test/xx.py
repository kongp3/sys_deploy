# -*- coding:utf-8 -*-
from fabric.api import env
DEPLOY_FLAG = 'test'  # 这个标识起得作用就是提示

# ############################ 服务器 信息 ########################################
SERVER1_USER = 'admin'
SERVER1_IP = 'xxx.xxx.xxx.xxx'
SERVER1_PWD = 'SERVER1_PWD'

SERVER2_USER = 'admin'
SERVER2_IP = 'xxx.xxx.xxx.xxx'
SERVER2_PWD = 'SERVER2_PWD'

SERVER3_USER = 'admin'
SERVER3_IP = 'xxx.xxx.xxx.xxx'
SERVER3_PWD = 'SERVER3_PWD'

# ############################ MySQL 信息 ########################################
MYSQL_HOST = 'MYSQL_HOST'
MYSQL_USER = 'MYSQL_USER'
MYSQL_PASS = 'MYSQL_PASS'

# ############################ Redis 信息 ########################################
REDIS_HOST = 'REDIS_HOST'
REDIS_USER = 'REDIS_USER'
REDIS_PASS = 'REDIS_PASS'
REDIS_PORT = 'REDIS_PORT'

# ############################ MongoDB 信息 ########################################
MONGODB_HOST = 'MONGODB_HOST'
MONGODB_PORT = 'MONGODB_PORT'
MONGODB_USER = 'MONGODB_USER'
MONGODB_PASS = 'MONGODB_PASS'


# ############################ OSS 信息 ########################################
OSS_BUKET = 'OSS_BUKET'
OSS_ENDPOINT = 'OSS_ENDPOINT'

# ############################ 远程访问配置 ########################################
env.passwords[SERVER1_USER + '@' + SERVER1_IP + ':22'] = SERVER1_PWD
env.passwords[SERVER2_USER + '@' + SERVER2_IP + ':22'] = SERVER2_PWD
env.passwords[SERVER3_USER + '@' + SERVER3_IP + ':22'] = SERVER3_PWD
env.key_filename = '~/.ssh/id_rsa.pub'
