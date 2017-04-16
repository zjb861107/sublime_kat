# -*- coding: utf8 -*-
import os
import re
import sublime
import sublime_plugin
from .errors import *

SETTINGS = sublime.load_settings('XTestPlugin.sublime-settings')
ADB = SETTINGS.get('adb')


# TODO:add logging file handler

def setup_adb(adb_path):
    sublime.platform()
    # TODO：检查adb可用性
    pass


def multiple_adb():
    # TODO：多个设备时需要选择
    pass


def list_dir(dir_path):
    assert os.path.exists(dir_path) and os.path.isdir(dir_path)
    res = []
    for i in os.listdir(dir_path):
        path = os.path.join(dir_path, i)
        if os.path.isfile(path):
            res.append(path)
        else:
            res += list_dir(path)
    return res


def push_files(adb, file_list):
    white_list = sublime.load_settings('XTestPlugin.sublime-settings').get("files_white_list")
    black_list = sublime.load_settings('XTestPlugin.sublime-settings').get("files_black_list")

    def filter_by_re(text, pattern_list):
        for pattern in pattern_list:
            p = re.compile(str(pattern))
            if p.search(text):
                return True
        else:
            return False

    white = filter(lambda x: filter_by_re(x, white_list), file_list)
    black = filter(lambda x: filter_by_re(x, black_list), file_list)
    files = set(file_list) - set(black) | set(white)
    # for i in files:
    #     print(i)
    # TODO:封装adb命令


class ExampleCommand(sublime_plugin.WindowCommand):
    # TODO：如果执行时，缓冲区更改未保存，则给出提示
    def run(self):
        print(self.__class__.__name__)
        self.window.set_sidebar_visible(True)  # 设置打开sidebar

        # 确定文件（脚本）路径
        files_root_path = None
        current_file_path = self.window.active_view().file_name()
        if current_file_path:
            files_root_path = os.path.dirname(current_file_path)
        else:  # 如果未打开任何文件（无任何文件在编辑状态）
            if len(self.window.folders()) > 1:
                sublime.error_message(too_many_files_or_folders)
            elif len(self.window.folders()) < 1:
                sublime.error_message(no_file_or_folder)
            else:
                files_root_path = self.window.folders()[0]  # 只有一个文件夹的情况
        # print(files_root_path)
        files = list_dir(files_root_path)
        push_files(ADB, file_list=files)


class DoctorCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print(self.__class__.__name__)
        print("sublime version:{0}, sublime channel:{1}".format(sublime.version(), sublime.channel()))
        print("Platform:{0}\nArch:{1}\n".format(sublime.platform(), sublime.arch()))
        # TODO:从packages.json读取版本号
