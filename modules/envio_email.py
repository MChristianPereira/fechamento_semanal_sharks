import os
import smtplib
from email.message import EmailMessage

class enviar_email():
    def __init__(self):

        self.remetente = os.getenv('EMAIL_REMETENTE')
        self.destinatario = os.getenv('EMAIL_DESTINATARIO')
        self.senha_email_remetente = os.getenv('SENHA_EMAIL_REMETENTE')
        self.enviando_email()

    def enviando_email(self):

        msg = EmailMessage()
        msg['Subject']  = 'FECHAMENTO SEMANAL'
        msg['From'] = self.remetente
        msg['To'] = self.destinatario

        with open('archives/fechamento_semanal_acoes.png', 'rb') as content_file:
            content = content_file.read()
            msg.add_attachment(content, maintype='application', subtype='png', filename='fechamento_semanal_acoes.png')

        with open('archives/ibov.png', 'rb') as content_file:
            content = content_file.read()
            msg.add_attachment(content, maintype='application', subtype='png', filename='ibov.png')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.remetente, self.senha_email_remetente)
            smtp.send_message(msg)
            print('E-mail enviado com sucesso!')
    
    def enviando_erro_email(self, error):
            
            msg = EmailMessage()
            msg['Subject']  = 'ERRO NO FECHAMENTO SEMANAL'
            msg['From'] = self.remetente
            msg['To'] = self.remetente

            msg.set_content(f'{error}')

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.remetente, self.senha_email_remetente)
                smtp.send_message(msg)

if __name__ == '__main__':
    enviar_email()