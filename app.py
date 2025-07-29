import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Message
from werkzeug.utils import secure_filename
import psycopg2  
from psycopg2.extras import RealDictCursor
from datetime import datetime


app = Flask(__name__)

# Pasta onde as imagens serão salvas
UPLOAD_FOLDER = os.path.join('static', 'img', 'upload')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Rota principal (home)
@app.route('/')
def index():
    try:
        conn = psycopg2.connect(
            dbname="ibfescola",
            user="postgres",
            password="142536",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM carousel ORDER BY id DESC")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        # Transformar os dados em lista de dicionários
        slides = [dict(zip(columns, row)) for row in rows]

        conn.close()
        return render_template('index.html', slides=slides)

    except Exception as e:
        erro_msg = str(e).encode('utf-8', errors='replace').decode('utf-8', errors='replace')
        return f"<h3 style='text-align:center;'>Erro ao carregar slides: {erro_msg}</h3>"

# Rota de login admin
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['password']

        try:
            conn = psycopg2.connect(
                dbname="ibfescola",
                user="postgres",
                password="142536",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE username = %s AND password = %s", (usuario, senha))
            resultado = cursor.fetchone()
            conn.close()

            if resultado:
                return redirect('/painel')
            else:
                return "<h3 style='text-align:center;'>Login inválido!</h3>"
        except Exception as e:
            erro_msg = str(e)
            print(f"ERRO: {erro_msg}")  # Isso vai aparecer no terminal
            return f"<h3 style='text-align:center;'>Erro ao salvar no banco: {erro_msg}</h3>"

    return render_template('login.html')



@app.route('/painel')
def painel():
    try:
        conn = psycopg2.connect(
            dbname="ibfescola",
            user="postgres",
            password="142536",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM carousel ORDER BY id DESC")
        slides = cursor.fetchall()
        conn.close()
        return render_template('painel.html', slides=slides)

    except Exception as e:
        erro_msg = str(e)
        print(f"ERRO ao conectar com o banco: {erro_msg}")
        return f"<h3 style='text-align:center;'>Erro ao conectar com o banco: {erro_msg}</h3>"


@app.route('/upload-image', methods=['POST'])
def upload_image():
    imagem = request.files['image']
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    link = request.form['link']  # Certifique-se que o campo "link" existe no formulário

    if imagem:
        nome_seguro = secure_filename(imagem.filename)

        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        caminho_imagem = os.path.join(app.config['UPLOAD_FOLDER'], nome_seguro)
        imagem.save(caminho_imagem)

        caminho_relativo = os.path.join('img', 'upload', nome_seguro).replace("\\", "/")

        try:
            conn = psycopg2.connect(
                dbname="ibfescola",
                user="postgres",
                password="142536",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO carousel (titulo, descricao, imagem, link) VALUES (%s, %s, %s, %s)",
                (titulo, descricao, caminho_relativo, link)
            )
            conn.commit()
            conn.close()

            return redirect('/painel')

        except Exception as e:
            erro_msg = str(e)
            print(f"ERRO ao salvar no banco: {erro_msg}")
            return f"<h3 style='text-align:center;'>Erro ao salvar no banco: {erro_msg}</h3>"

    return "<h3 style='text-align:center;'>Erro: imagem não enviada.</h3>"


@app.route('/excluir/<int:slide_id>', methods=['POST'])
def excluir_slide(slide_id):
    try:
        conn = psycopg2.connect(
            dbname="ibfescola",
            user="postgres",
            password="142536",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Buscar o nome da imagem antes de excluir o registro
        cursor.execute("SELECT imagem FROM carousel WHERE id = %s", (slide_id,))
        resultado = cursor.fetchone()

        # Se tiver imagem salva, tenta excluir o arquivo físico
        if resultado and resultado[0]:
            caminho_imagem = os.path.join('static', resultado[0])
            if os.path.exists(caminho_imagem):
                os.remove(caminho_imagem)

        # Excluir o registro do banco
        cursor.execute("DELETE FROM carousel WHERE id = %s", (slide_id,))
        conn.commit()
        conn.close()

        return redirect('/painel')

    except Exception as e:
        erro_msg = str(e)
        print(f"ERRO ao excluir slide: {erro_msg}")
        return f"<h3 style='text-align:center;'>Erro ao excluir: {erro_msg}</h3>"


@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        try:
            from app import mail  # Importa o objeto mail configurado no app.py

            nome = request.form.get('nomesobrenome')
            email = request.form.get('email')
            telefone = request.form.get('telefone')
            mensagem = request.form.get('mensagem')
            curso = request.form.get('cursosescolhidos')
            horario = request.form.get('horario')
            modalidade = request.form.get('modalidade')
            ip = request.remote_addr

            msg = Message(
                subject='Novo Formulário de Contato',
                sender='novoalunoaqui@gmail.com',
                recipients=['lucasr.prodata@gmail.com']
            )
            msg.body = f"""
            Nome: {nome}
            E-mail: {email}
            Telefone: {telefone}
            Mensagem: {mensagem}
            Curso Escolhido: {curso}
            Horário Preferido: {horario}
            Modalidade do Curso: {modalidade}
            IP: {ip}
            Enviado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
            """
            mail.send(msg)
            return redirect(url_for('contato', success=True))

        except Exception as e:
            return render_template('contato.html', erro_envio=True)

    return render_template('contato.html')






# Executa o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)