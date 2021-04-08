import discord
from discord.message import MessageType
import os.path


emails = list()

if os.path.isfile('emails.txt'):
    with open('information-from-email.txt') as file:
        for line in file:
            emails.append(line)


def write_emails(mails, *args):
    for arg in args:
        mails.remove(arg)
    for mail in mails:
        with open('emails.txt','w') as f:
            f.write(mail+"\n")


def send_email(recipient, body):

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    print("message: ")
    print(body+"\n")
    print("------")

    gmail_user = 'beatsupcollective.id@gmail.com'
    gmail_pwd = 'djidan241201'
    FROM = 'Muhammad Djidan'
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = 'New Information from Beats Up EMAIL!!!'

    msg = MIMEMultipart()
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = recipient
    msg.attach(MIMEText(body,'plain'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, msg.as_string())
        server.close()
        print("successfully sent the mail to "+recipient)
    except: print("failed to send mail to "+recipient)

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content == "!list":
        for email in emails:
            await client.send_message(message.channel, content=str(email))

    elif message.content[:4] == "!add":
        print("Added "+message.content[5:]+" to emails")
        emails.append(message.content[5:])
        write_emails(emails)

    elif message.content[:4] == "!del":
        print("Removed "+message.content[5:]+" from emails")
        write_emails(emails, message.content[5:])

    elif message.type is MessageType.default:
        if str(message.author) != 'Beats Up Dev. Bot':
            for email in emails:
                send_email(email, message.content)


client.run('ODI5NjY5ODU3MTI4NzQyOTEy.YG7gRA.Izo6cRcp-FeHufXmaLn-h2RhkY0')
