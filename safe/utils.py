import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.mime.image import MIMEImage
import cv2


def send_email(subject, message):

    try:
        my_sender = '1158677160@qq.com'  # 邮件发送者
        my_pass = 'Lly19980726.'  # 邮件发送者邮箱密码
        my_user = '13777893886@163.com'
        msg = MIMEText(message, 'html', 'utf-8')
        msg['From'] = formataddr(["From Safe Home", my_sender])
        msg['To'] = formataddr(["Client", my_user])
        msg['Subject'] = subject

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        server.quit()
        print("---邮件发送成功---")
    except Exception as e:
        print(e, "---邮件发送失败---")


def send_html_email(subject, message, image):

    try:
        my_sender = '1158677160@qq.com'  # 邮件发送者
        my_pass = 'Lly19980726.'  # 邮件发送者邮箱密码
        my_user = '13777893886@163.com'

        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = subject
        msgRoot['From'] = formataddr(["From Safe Home", my_sender])
        msgRoot['To'] = formataddr(["Client", my_user])

        msgText = MIMEText(f"""
                    {message}
                """, 'html', 'utf-8')

        msgRoot.attach(msgText)
        msgImage = MIMEImage(cv2.imencode('.jpg', image)[1].tobytes())    # or tostring?
        msgImage.add_header('Content-ID', '')
        msgRoot.attach(msgImage)

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, [my_user, ], msgRoot.as_string())
        server.quit()
        print("---邮件发送成功---")
    except Exception as e:
        print(e, "---邮件发送失败---")
