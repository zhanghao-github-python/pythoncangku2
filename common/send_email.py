# =================conding: utf-8
"""
================================================================================

Author : Administrator
Created  on : 2020/11/29

E-mail: zh13997821732@163.com


================================================================================

"""

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import win32com.client as win32


class SendEmail(object):

    @staticmethod
    def send_qq_file_mail(title, message, file_path, file_name):
        # 创建一个SMTP对象 连接SMTP服务
        s = smtplib.SMTP_SSL('smtp.qq.com', 465)

        msg_from = '769314439@qq.com'
        passwd = 'dmbehavbprowbfha'

        msg_to = ['3023087535@qq.com']

        s.login(user=msg_from, password=passwd)

        # 构建邮件内容 附件
        content = MIMEText(message, _charset='utf8')

        part = MIMEApplication(open(file_path, 'rb').read())
        # 自定义文件名称
        part.add_header('content-disposition', 'attachment', filename=file_name)

        # 封装邮件 添加主题
        msg = MIMEMultipart()
        # 向邮件添加内容和附件
        msg.attach(content)
        msg.attach(part)

        # 设置邮件显示参数
        msg['Subject'] = Header(title, 'utf-8')
        msg['From'] = msg_from
        # 接收的参数类型 '3023087535@qq.com, 1235425@qq.com'
        msg['To'] = ','.join(msg_to)

        # 发送邮件
        try:
            s.sendmail(from_addr=msg_from, to_addrs=msg_to, msg=msg.as_string())
            print('Send Email Successfully')
        except Exception as e:
            print('Send Email Failed')
            raise e
        finally:
            s.quit()

    @staticmethod
    def send_outlook_file_mail(mail_title, mail_message, file_path):

        addressee = '3023087535@qq.com' + ';' + 'zu2019@outlook.com'  # 收件人邮箱列表
        cc = 'tomcat666888@163.com' + ';' + '87313199@qq.com'  # 抄送人邮件列表
        mail_path = file_path  # 获取测试报告路径
        olook = winc32.Dispatch("outlook.Application")  # 固定写法
        mail = olook.CreateItem(0)  # 固定写法
        mail.To = addressee  # 收件人
        mail.CC = cc  # 抄送人
        # mail.Recipients.Add(addressee)
        mail.Subject = mail_title  # 邮件主题
        # mail.Attachments.Add(mail_path, 1, 1, "myFile")
        mail.Attachments.Add(mail_path)
        read = open(mail_path, encoding='utf-8')  # 打开需要发送的测试报告附件文件
        # content = read.read()  # 读取测试报告文件中的内容
        read.close()
        mail.Body = mail_message  # 将从报告中读取的内容，作为邮件正文中的内容
        try:
            mail.Send()  # 发送
            print("send outlook_email successfully")

        except Exception as e:
            print("send outlook_email failed")
            raise e


if __name__ == '__main__':
    import os
    from common.constant import CONF_DIR

    title = '这是测试邮件'
    message = '这是测试邮件内容'
    file_path = os.path.join(CONF_DIR, 'config_test.ini')
    file_name = 'test.html'
    SendEmail.send_qq_file_mail(title, message, file_path, file_name)
