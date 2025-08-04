from flask import Flask
from config import UPLOAD_FOLDER
from db import init_db
from routes import register_routes
from mail_config import init_mail, mail

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

init_db()
init_mail(app)
register_routes(app)

# Torna o objeto mail acessível em outros módulos
app.mail = mail

if __name__ == '__main__':
    app.run(debug=True)