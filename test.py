import smtplib
smtp = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=10)
smtp.login("61206264@qq.com", "dvkjelmwvcxrbicg")
smtp.quit()