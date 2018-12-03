# 一、解决什么问题

* **把上传到gitlab的代码放到生产(或测试)服务器上** 

# 二、需要哪些步骤(理论)

* 写好配置文件模板
* 使用部署脚本的指令执行(弄到服务器、安装依赖库、启动服务都在脚本里搞定)
* 如果出现错误，本地修改，上传后重新部署，保证本地代码和git、线上同步

# 三、起到什么作用
1. 从配置文件角度规范代码
2. 保护服务器和数据库信息
3. 每个人能自己部署, 提高效率

# 四、需要什么步骤(命令)
1. **登录部署服务器**
```
$ ssh admin@deploy.transfereasy.com
```

2. **进入部署目录**
```
~$ cd
~$ cd sys_deploy
~/sys_deploy$
```

3. **查看帮助**
```
~/sys_deploy$ fab help
```

4. **查看可部署项目**
```
~/sys_deploy$ fab -f xx.py -l
```

5. **选一个项目部署**
```
~/sys_deploy$ fab -f xx.py php_sys
```


# 五、做好哪些准备

## 1. deploy.yaml文件
* 1) 在项目根目录下新建`deploy.yaml`文件
* 2) Python项目内容如下

```
config:
   - py_sys/config/configuration.py  # 你的配置文件从项目目录开始的相对路径, 这里可写任意个，'-'作为起始标识
supervisord:
   group: py  # 你的supervisord服务的分组
env:
   dir: ENV # 你的virtualenv目录名
```

* 3) php 项目内容如下

```
config:
    - sys_deploy/config/app.php
    - sys_deploy/config/variable.php   
```

## 3. 编写配置文件模板

* **原则**
* 1) 不区分生产和测试环境的配置直接写死
* 2) 区分生产和测试环境但是与IP、域名、数据库、内存等服务器相关的设计替换符来替换
* 3) 区分生产和测试环境但是与业务数据相关的，用$ENV_FLAG$来区分

* **举例**

```
Python：
MYSQL_HOST = '$MYSQL_HOST$'  
MYSQL_USER = '$MYSQL_USER$'  
MYSQL_PASS = '$MYSQL_PASS$' 
```

```
Php：

'Datasources' => [
    'default' => [
        'className' => 'Cake\Database\Connection',
        'driver' => 'Cake\Database\Driver\Mysql',
        'persistent' => false,
        'host' => '$MYSQL_HOST$',     
        'username' => '$MYSQL_USER$', 
        'password' => '$MYSQL_PASS$', 
        ...
]
```

* 看如下代码及注释

```
Python:

ENV_FLAG = '$ENV_FLAG$'       # 这里部署之后会被替换成 'prod' 或 'test' 下面可以根据这两个环境来判断
if ENV_FLAG == 'prod':
    ALERT_TARGET_LIST = [
        'ww@tt.com',
        'mm@kk.com'
    ]
else:
    ALERT_TARGET_LIST = [
        'mm@kk.com',
    ]
```

```
php:

$envFlag = '$ENV_FLAG$';    // 这里部署之后会被替换成 'prod' 或 'test' 下面可以根据这两个环境来判断

if ($envFlag == 'prod') {
    $header = [
        'X-Agent-No'=>'HI58240389a6062',
        'X-Agent-Secret'=>'tea_bZ94UNDsXsJ2M3FGmb8I',
        'X-Api-Version'=>'v1'
    ];
}
else {
    $header = [
        'X-Agent-No'=>'TEST',
        'X-Agent-Secret'=>'tea_oA0OkdMs0x7EGRP0P5Hr',
        'X-Api-Version'=>'v1'
    ];
}

```
## 4. Python项目需要添加依赖库文件
* 每个Python项目需要在项目的根目录下建立 `requirements.txt` 
* 内容是此项目运行需要的所有依赖库
* 文件缺失部署会失败
* 内容不全代码无法运行
