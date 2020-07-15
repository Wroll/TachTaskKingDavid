import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup

ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "randomchipchip" + ORG_EMAIL
FROM_PWD = "852456852456qw"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 993


class LinkFromVerificationMessage:

    @staticmethod
    def get_link():
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()
        # print(id_list)
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        try:
            for i in range(latest_email_id, first_email_id, -1):
                typ, data = mail.fetch(str(i), '(RFC822)')
                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject = decode_header(msg["Subject"])[0][0]
                        if isinstance(subject, bytes):
                            # if it's a bytes, decode to str
                            subject = subject.decode()
                        if msg.is_multipart():
                            # iterate over email parts
                            for part in msg.walk():
                                # extract content type of email
                                content_type = part.get_content_type()
                                if content_type == "text/html":
                                    body = part.get_payload(decode=True).decode()
                                    soup = BeautifulSoup(body, 'html.parser')
                                    link = soup.find(text='Click here', href=True)
                                    if link:
                                        return link['href']

        except TypeError as ex:
            print(str(ex), 'link to verification message not presented')
            return False


# if __name__ == '__main__':
#     print(GetLinkFromVerificationMessage.get_link())