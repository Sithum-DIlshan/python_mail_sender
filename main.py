from fastapi import FastAPI, UploadFile

app = FastAPI()
import smtplib
from email.message import EmailMessage
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# from dbconnect import insertData
import ssl
import smtplib
import pytracking



email_sender = "sithumd@kainovation.com"
email_password = "jbjxgtkvbyhmzlbe"

email_reciever = "sithumdilshan985@gmail.com"

subject = "sending"
# body = """
#     This is testing
# """

# filename = "sample.pdf"

# with open(filename, "rb") as attachment:
#     # Add file as application/octet-stream
#     # Email client can usually download this automatically as attachment
#     part = MIMEBase("application", "octet-stream")
#     part.set_payload(attachment.read())

# # Encode file in ASCII characters to send by email
# encoders.encode_base64(part)

# # Add header as key/value pair to attachment part
# part.add_header(
#     "Content-Disposition",
#     f"attachment; filename= {filename}",
# )

# em.attach(part)

# open_tracking_url = pytracking.get_open_tracking_url(
    #     {"customer_id": 1}, base_open_tracking_url="https://trackingdomain.com/path/",
    #     webhook_url="http://requestb.in/123", include_webhook_url=True
    #     )
    # print(open_tracking_url)
    # full_url = "https://trackingdomain.com/path/eyJtZXRhZGF0YSI6IHsiY3VzdG9tZXJfaWQiOiAxfSwgIndlYmhvb2siOiAiaHR0cDovL3JlcXVlc3RiLmluLzEyMyJ9"
    # tracking_result = pytracking.get_open_tracking_result(
    # full_url, base_open_tracking_url="https://trackingdomain.com/path/")
    # print(tracking_result)

context = ssl.create_default_context()


def finalize_mailsend(file: UploadFile, message: str, email: str):
    
    em = MIMEMultipart()
    em["From"] = email_sender
    em["To"] = email_reciever
    em["subject"] = subject
    em["Disposition-Notification-To"] = email_sender

    body = message
    em.attach(MIMEText(body, "plain"))
    filename = file.filename
    html = """\
<html>
  <head></head>
  <body>
    <img src="https://www.w3schools.com/images/lamp.jpg" alt="Lamp" width="30" height="30">
  </body>
</html>
"""
    em.attach(MIMEText(html, "html"))

    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(file.file.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    em.attach(part)
    part = "null"
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email, em.as_string())
        # insertData(email_sender, email)


@app.post("/my-first-api")
def sendmail(email: str, message: str, file: UploadFile):
    message = (
        message
    )
    finalize_mailsend(file, message, email)
    return {"filename": file.filename}


@app.get("/")
def emailgather():
    print("hello")
    return {"Hello"}
