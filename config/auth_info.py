# -*- coding: utf-8 -*-
from config import *

# ################## 这里两个$符号之间的文字是用来替换每个项目的配置文件的 ############################
# ################## 开发工程师在自己的配置文件里写好模板, 服务器信息由运维工程师维护 ############################
# ################## 可以根据自己业务情况扩展 ############################

auth_info = {
    "$ENV_FLAG$": DEPLOY_FLAG,

    "$MYSQL_HOST$": MYSQL_HOST,
    "$MYSQL_USER$": MYSQL_USER,
    "$MYSQL_PASS$": MYSQL_PASS,

    "$MONGO_HOST$": MONGODB_HOST,
    "$MONGO_USER$": MONGODB_USER,
    "$MONGO_PASS$": MONGODB_PASS,
    "$MONGO_PORT$": MONGODB_PORT,

    "$REDIS_HOST$": REDIS_HOST,
    "$REDIS_USER$": REDIS_USER,
    "$REDIS_PASS$": REDIS_PASS,
    "$REDIS_PORT$": REDIS_PORT,

    "$OSS_BUCKET_PRIVTE$": OSS_BUKET,
    "$OSS_ENDPOINT$": OSS_ENDPOINT,

}
