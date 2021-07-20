

# 加载第三方包
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from config.log_config import logger

class Email:

    # 第三方服务信息
    async def sendEmail(self, send_name, header_name, email, content=''):
        '''
        :param send_name string 发送者名称
        :param header_name string 邮件标题
        :param eamil string 接收者邮箱地址
        :param content string 需要发送的内容
        '''
        # 第三方 SMTP 服务
        mail_host="smtp.qq.com"  #设置服务器
        mail_user="26152462@qq.com" #    #用户名
        mail_pass="qzmlnvtojjkgbhbb"   #口令 - 腾讯授权

        sender = '26152462@qq.com'      # 发送者邮箱地址
        receivers = [email]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

        # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
        message = MIMEText(content, 'plain', 'utf-8')

        message['From'] = Header(send_name, 'utf-8')   # 发送者
        message['To'] =  Header(email, 'utf-8')        # 接收者

        title = header_name
        message['Subject'] = Header(title, 'utf-8')

        try:
            smtpObj = smtplib.SMTP() 
            smtpObj.connect(mail_host, 587)    # 25 为 SMTP 端口号
            smtpObj.login(mail_user,mail_pass)  
            smtpObj.sendmail(sender, receivers, message.as_string())
            logger.info("邮件发送成功")
            return 1
        except smtplib.SMTPException:
            logger.info("Error: 无法发送邮件")
            return 0





email = Email()


# 备份原生邮箱发送系统
# class Email:

#     # 第三方服务信息
#     async def sendEmail(self, send_name, header_name, email, content=''):
#         '''
#         :param send_name string 发送者名称
#         :param header_name string 邮件名称
#         :param eamil string 接收者邮箱地址
#         :param content string 需要发送的内容
#         '''
#         # 第三方 SMTP 服务
#         mail_host="smtp.qq.com"  #设置服务器
#         mail_user="26152462@qq.com" #    #用户名
#         mail_pass="qzmlnvtojjkgbhbb"   #口令 - 腾讯授权

#         sender = '26152462@qq.com'      # 发送者邮箱地址
#         receivers = ['26152462@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

#         # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
#         message = MIMEText('Dash项目 邮件发送测试...', 'plain', 'utf-8')

#         message['From'] = Header("达世科达", 'utf-8')   # 发送者
#         message['To'] =  Header('2623', 'utf-8')        # 接收者

#         header_name = 'Dash项目 SMTP 邮件系统测试'
#         message['Subject'] = Header(header_name, 'utf-8')

#         try:
#             smtpObj = smtplib.SMTP() 
#             smtpObj.connect(mail_host, 587)    # 25 为 SMTP 端口号
#             smtpObj.login(mail_user,mail_pass)  
#             smtpObj.sendmail(sender, receivers, message.as_string())
#             # logger.info("邮件发送成功")
#             return 1
#         except smtplib.SMTPException:
#             # logger.info("Error: 无法发送邮件")
#             return 0





# email = Email()