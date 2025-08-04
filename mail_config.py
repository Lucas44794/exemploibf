from flask_mail import Mail

mail = Mail()

def init_mail(app):
    app.config.update(
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME='novoalunoaqui@gmail.com',  # Seu e-mail
        MAIL_PASSWORD='sua_senha_de_app',         # Senha de app gerada no Gmail
        MAIL_DEFAULT_SENDER='novoalunoaqui@gmail.com'
    )
    mail.init_app(app)