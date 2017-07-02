##### CONFIG ###############
user = 'username' 
my_pw = 'mailpassword'
folder = 'foldername where poe mails get in' ## z.b 'Spam'
imapserver = 'imap server' ## z.b'imap.web.de'
imapport = '993' ## z.b 993 is default port
#############################

import imaplib

def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

def fdelete_mail(mb, uid):
    mb.uid('STORE', uid, '+FLAGS', '(\\Deleted)')
    mb.expunge()

def get_code(mailstruct):
    raw_email = mailstruct[0][1]
    rawbody=raw_email.decode()
    x=rawbody.find(':=0A=0A')
    code=rawbody[x+7:x+19]
    return code


install_and_import('pyperclip')

#Connect to Server and get uid from unseen mail with POE Subject
#TODO:There could be more than 1 unseen Mail.
mailbox = imaplib.IMAP4_SSL(imapserver,imapport)
mailbox.login(user, my_pw)
mailbox.select(ordner)
result, mail_ids = mailbox.uid('search', None, '(HEADER Subject "Path of Exile Account Unlock Code" UNSEEN)')

if len(mail_ids[0])!=0:
    latest_email_uid = mail_ids[0].split()[-1]
    result, data = mailbox.uid('fetch', latest_email_uid,"(UID BODY[TEXT])")
    code = get_code(data)
    pyperclip.copy(code)
    print('Your Code: '+ code + ' is copied to your clipboard !')
    if delete_mail:
        fdelete_mail(mailbox, latest_email_uid)
        print('Delete Mail...Done')
else:
    print('No new Path of Exile mails found!')

mailbox.close()
mailbox.logout()
input()

