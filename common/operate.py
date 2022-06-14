"""
根据tool 封装常用方法
"""
import pymysql, pyperclip, os, paramiko
import pyzbar.pyzbar as pyzbar
from PIL import Image



class SumOperate:
    """ 其他 常用 非 selenium 类方法 """
   
    @staticmethod
    def get_2fa(code : str):
        """ 执行2fa 获取 验证码"""
        result = os.popen(f'kmg 2fa {code}').read()
        return result

    @staticmethod
    def mysql_opreate(ip:str="139.224.239.215", user:str="root", pw:str=None, dbname:str=None, sql:str=None):
        db = pymysql.connect(host=ip, user=user, password=pw, database=dbname)

        cursor = db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()

        db.close()
        return data

   

    @staticmethod
    def get_img_info(path:str):
        """
        识别二维码
        """
        img = Image.open(path)
        img.show()
        barcodes = pyzbar.decode(img)
        for x in barcodes:
            return x.data.decode("utf-8")

    @staticmethod
    def get_clip_text():
        print(pyperclip.paste())
        return pyperclip.paste()

    @staticmethod
    def ssh_server(ip, port, username, pw ,cmd):
        """远程连接 服务器， 执行相关命令 """
        # 生成SSH客户端
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(ip, port, username, password=pw)
        stdin,stdout,stderr = s.exec_command(cmd)
        p = stdout.read()
        s.close()
        return p
    
  

    @staticmethod
    def logmsg(msg: str):
        """
        对rais msg 进行处理后存入log 中
        """
        txt = msg.split(r'> File', 1)
        return txt[-1]


