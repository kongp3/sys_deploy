# -*- coding: utf-8 -*-

from fabric.contrib.files import *


def t_mkdir(new_dir_path):
    if exists(new_dir_path) is False:
        run('mkdir ' + new_dir_path)


def t_chmod(dec_dir, permission, option=''):
    run('chmod ' + option + ' ' + permission + ' ' + dec_dir, warn_only=True, quiet=True)


def t_cp(sou_dir, dec_dir, option):
    run('cp ' + option + ' ' + sou_dir + ' ' + dec_dir)


def t_rm(dec_dir, option):
    try:
        sudo('rm ' + option + ' ' + dec_dir)
    except Exception, e:
        print e


def t_mv(sou_file, dec_file,):
    print exists(sou_file)
    if dec_file == '*' or exists(sou_file):
        sudo('mv ' + sou_file + ' ' + dec_file)

