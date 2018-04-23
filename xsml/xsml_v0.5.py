# --coding:utf-8--
import os
import re
import shutil
from soup_tool import MyThread
from time import ctime, sleep
from datetime import datetime
import time

# from pinyin import pinyin

'''
title:根据data_path.md中的小说路径，生成HTML电子
version:0.3 MAC下，在读取生成HTML电子书，将电子书模板搬运到小说目录后
version:0.4 在同级目录下生成Yao's电子书
version:0.5 去除content中的\xa0、\n、\t等字符
author:yaowei
date:2018-04-15
'''


class Xsread:
    def __init__(self):

        """
         如果使用绝对路径来加载资源，
            则在mac上只能以拖拽方式将HTML放入浏览器中打开
        """
        path = str(os.getcwd()) + "/Yao's电子书/"
        self.mod_path = path  # 模板路径
        self.list_mod_path = self.mod_path + '/list_mod.html'
        self.con_mod_path = self.mod_path + '/con_mod.html'
        self.md_file = 'data_path.md'  # 小说根目录绝对路径

        # 初始化读取配置文件 第一行数据
        self.root_read_path = self.__read_file(self.md_file)[0]

        # 初始化读取list_mod.html
        self.list_mod_html = self.__read_file(self.list_mod_path)
        # 初始化读取con_mod.html
        self.con_mod_html = self.__read_file(self.con_mod_path)

        # 小说指南路径
        self.tree_path = ''

        # mac\liunx 文件目录为／ windows为\
        arr = self.root_read_path.split('/')
        self.root_rela_path = arr[len(arr) - 1]

        # 初始化创建 电子书根目录 与小说目录平级
        self.root_dzs_mod_path = self.root_read_path.rstrip(self.root_rela_path) + "/Yao's电子书/"
        # 先删除，再创建
        self._drop_folder(self.root_dzs_mod_path)
        # 复制模板到电子书根目录
        print(self.mod_path, self.root_dzs_mod_path)
        self._copy_folder(self.mod_path, self.root_dzs_mod_path)

        # 添加多线程
        self.threads = []

    @staticmethod
    def __read_file(path):
        list_mod = open(path, 'r', encoding='utf-8')
        list_html = list_mod.readlines()
        list_mod.close()
        return list_html

    def _dir_list(self, path='', time_=2):
        """
           递归遍历小说目录，创建HTML电子书
           :type time_: object 线程休眠时间
           :type path: object
        """

        if '' is path:
            dir_name = self.root_read_path
        else:
            dir_name = path

        if os.path.isdir(dir_name):
            # 目录
            files = os.listdir(dir_name)

            # 文件名排序
            files.sort()

            json_data = {'isdir': 'Y', 'dir_name': dir_name, 'files': files}

            self._create_list_mod(json_data, time_)
            #t = MyThread(self._create_list_mod, (json_data, time_), self._create_list_mod.__name__)
            #self.threads.append(t)

            for file in files:
                if file in "Yao's电子书":
                    continue

                # 下级目录tree_path
                # 递归遍历文件目录
                self._dir_list(dir_name + '/' + file)

                #t = MyThread(self._dir_list, (dir_name + '/' + file, time_), self._dir_list.__name__)
                #self.threads.append(t)
        else:
            pass

    def _create_list_mod(self, json_data, time_):

        #sleep(time_)

        dir_name = json_data['dir_name']
        files = json_data['files']
        html_con = self.list_mod_html
        dd_html = ''

        # 切分根目录
        dir_arr = dir_name.split(self.root_rela_path)
        print('dir_arr', dir_arr)
        list_name = self.root_rela_path + dir_arr[len(dir_arr) - 1]
        now_path = self.root_dzs_mod_path + list_name + '/'
        print('list_name,-----------', list_name)
        # 创建下级目录
        file_path = now_path
        self._create_folder(file_path)  # now_path =  dir_name

        list_arr = list_name.split("/")
        list_file_name = list_arr[len(list_arr) - 1]

        tree_path = ""
        rela_path = ""
        for cur_path in list_arr:
            print('cur_path-----------', cur_path)
            # 需要先替换当前根目录，因为cur_path中已经包含了
            rela_path += cur_path + '/'
            tree_path += '<a href="' + self.root_dzs_mod_path + '/' + rela_path + '/index.html">' + cur_path + "</a>&gt;"
        self.tree_path = tree_path

        print('tree_path ok')

        for dd in files:
            # 转换拼音，作为href
            # py = pinyin.get(dd, format="strip", delimiter="")

            # mac上特殊处理，文件夹下隐藏的文件
            if 'DS_Store' in dd:
                continue

            href = now_path + '/' + dd + '/'
            file_read_path = self.root_read_path + list_name.replace(self.root_rela_path, '') + '/' + dd

            a_text = dd.replace(".txt", "")

            print('file_read_path is ', file_read_path)

            # 如果此链接是文件，则html名改为文件名
            if os.path.isfile(file_read_path):
                print('is file')
                file_href = now_path + a_text
                new_href = file_href + '.html'
                self._con_mod(file_read_path, new_href, a_text)
            else:
                new_href = href + '/index.html'

            # 创建list a
            dd_html += '<dd><a href="' + new_href + '" >' + a_text + '</a></dd>'
        # end for ---------------------

        print('dd_html', dd_html)

        html_str = ''.join(html_con).replace('${file_name}', list_file_name) \
            .replace('${files}', dd_html) \
            .replace('${root_path}', self.root_dzs_mod_path) \
            .replace('${tree_path}', self.tree_path)

        # write 使用 根据目录名创建index.html
        write_file_path = now_path + 'index.html'  # 主页
        self._write_file(write_file_path, html_str)

        # 如果是根目录.html，则在电子书文件夹下同样创建一个html
        if rela_path in self.root_rela_path:
            self._write_file(write_file_path, html_str)

    def _con_mod(self, read_path, write_path, title):
        # 读取模板
        con_html = self.con_mod_html
        # 读取txt内容
        con = self.__read_file(read_path)
        # 去除\xa0、\t、\n
        con = str(con)
        con = con.replace('\\xa0', '&nbsp;')\
            .replace("\\n', '", '<br/>')\
            .replace('\\t', '&nbsp;&nbsp;&nbsp;&nbsp;')
        #con = con.replace("['", "").replace("]'", "")

        # 替换标记内容
        content = ''.join(con_html).replace('${content}', str(con)) \
            .replace('${file_name}', title) \
            .replace('${root_path}', self.root_dzs_mod_path) \
            .replace('${tree_path}', self.tree_path)
        # 写入文件
        self._write_file(write_path, content)

    @staticmethod
    def _create_folder(path):
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")
        rstr = r"[\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_path = re.sub(rstr, "_", path)  # 替换为下划线
        is_exists = os.path.exists(new_path)
        # 不存在则创建
        if not is_exists:
            os.makedirs(new_path)
            print('目录:', new_path + ' create')
        else:
            print(new_path + ' 目录已存在')

    @staticmethod
    def _drop_folder(path):
        is_file = os.path.exists(path)
        if is_file:
            shutil.rmtree(path)
        else:
            print('目录不存在')

    @staticmethod
    def _copy_folder(from_path, to_path):
        # copy整个目录
        shutil.copytree(from_path, to_path)

    @staticmethod
    def _write_file(file_path, content):
        path = file_path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")
        rstr = r"[\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_path = re.sub(rstr, "_", path)  # 替换为下划线，比文件夹多了正反斜杠(\/)去除

        file_object = open(new_path, 'w', encoding='utf-8')
        file_object.write(content)
        file_object.close()
        print('_write_file ', new_path)

    # end _oot_list_path  ---------------------------------------

    def run(self):
        try:

            now = int(time.time())
            print('now:', now)

            date = datetime.now()
            print('all begin ', ctime(), '开始生成！')

            self._dir_list('', 2)

            for t in self.threads:
                t.start()
            for t in self.threads:
                t.join()


            now2 = int(time.time())
            print('now2', now2)

            nowdate = now2 - now
            print('共', nowdate, '秒')

            print('all end ', ctime(), '生成完毕！')
        except BaseException as msg:
            print('msg : ', msg)
            pass


Xsread().run()
