import os
import pathlib
import smtplib
from string import Template
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

EMAIL_TEXT_PATH = pathlib.Path(__file__).parent / 'email.txt'


class Send_email():

    def __init__(self):
        load_dotenv()
        self.smtp_server = ''
        self.smtp_port = ''
        self.smtp_username = ''
        self.smtp_password = ''

        self.email_receiver = ''
        self.receiver_name = ''

# Metodo que executa todos os outros
    def run(self):
        self.insert_receiver_name()
        self.collect_email_receiver()
        self.smtp_config()
        self.email_text()
        self.create_mime()
        self.sending_email()

# metodo que coleta o nome do destinatario
    def insert_receiver_name(self):
        self.receiver_name = input('Qual nome do destinatario?')
        self.receiver_name.strip

# metodo que coleta o email do destinatario
    def collect_email_receiver(self):
        self.email_receiver = input('Qual o seu email?')
        self.email_receiver.strip
        self._verify_email_received()

# metodo que verifica o email recebido
    def _verify_email_received(self):
        if '@' and '.com' in self.email_receiver:
            print('email valido')
        else:
            print('Email invalido')
            self.collect_email_receiver()

# metodo que pega as configuracoes do arquivo .env
    def smtp_config(self):
        print('configurando conexão')
        self.smtp_server = os.getenv('SMTP_SERVER', '')
        self.smtp_port = os.getenv('SMTP_PORT', '')
        self.smtp_username = os.getenv('FROM_EMAIL', '')
        self.smtp_password = os.getenv('EMAIL_PASSWORD', '')
# metodo que define o texto do email

    def email_text(self):
        print('configurando conteudo do email')
        with open(EMAIL_TEXT_PATH, 'r', encoding='utf-8') as file:
            text_file = file.read()
            template = Template(text_file)
            text_email = template.substitute(nome=self.receiver_name)
            return text_email

# metodo que transforma tudo em um formato "enviavel" por email
    def create_mime(self):
        mime_multipart = MIMEMultipart()
        mime_multipart['from'] = os.getenv('FROM_EMAIL', '')
        mime_multipart['to'] = self.email_receiver
        mime_multipart['subject'] = 'E-mail Automatico'

        corpo_email = MIMEText(self.email_text(), 'html', 'utf-8')
        mime_multipart.attach(corpo_email)
        return mime_multipart

# metodo que envia o email
    def sending_email(self):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port,
                              context=context) as server:
            server.ehlo()
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(self.create_mime())
            print('E-mail enviado com  sucesso!')
