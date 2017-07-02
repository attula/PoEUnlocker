import imaplib
import pyperclip


##### CONFIG ###############
user = 'username' 
my_pw = 'mailpassword'
folder = 'foldername where poe mails get in' ## z.b 'Spam'
imapserver = 'imap server' ## z.b'imap.web.de'
imapport = '993' ## z.b 993 is default port
#############################

mailbox = imaplib.IMAP4_SSL(imapserver,imapport)
mailbox.login(user, my_pw)
mailbox.select(ordner)

result, mail_ids = mailbox.uid('search', None, '(HEADER Subject "Path of Exile Account Unlock Code")')
latest_email_uid = mail_ids[0].split()[-1]
result, data = mailbox.uid('fetch', latest_email_uid,"(UID BODY[TEXT])")
raw_email = data[0][1]
rawbody=raw_email.decode()
x=rawbody.find(':=0A=0A')
code=rawbody[x+7:x+19]
pyperclip.copy(code)

mailbox.uid('STORE',latest_email_uid, '+FLAGS', '(\\Deleted)')

mailbox.expunge()
mailbox.close()
mailbox.logout()

