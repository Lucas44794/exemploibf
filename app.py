import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import psycopg2  
from psycopg2.extras import RealDictCursor

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
        cursor.execute("DELETE FROM carousel WHERE id = %s", (slide_id,))
        conn.commit()
        conn.close()
        return redirect('/painel')
    except Exception as e:
        erro_msg = str(e)
        print(f"ERRO ao excluir slide: {erro_msg}")
        return f"<h3 style='text-align:center;'>Erro ao excluir: {erro_msg}</h3>"
    


# Executa o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)