from config import Options as op
import smtplib


def send_email(URL):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()

    msg = "\r\n".join([
      f"From: {op.EMAIL}",
      f"To: {op.EMAIL}",
      f"Subject: There are one or more available campsites at {op.LOCATION}!",
      "",
      f"Click on the link below to reserve your spot now.\n{URL}"
      ])

    server.login(op.EMAIL, op.APP_PASS)
    server.sendmail(op.EMAIL, op.EMAIL, msg)
    server.quit()