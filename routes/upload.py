import os
from flask import Blueprint, request, redirect, current_app
from werkzeug.utils import secure_filename
from db import get_connection

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload-image', methods=['POST'])
def upload_image():
    imagem = request.files['image']
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    link = request.form['link']

    if imagem:
        nome_seguro = secure_filename(imagem.filename)
        pasta_upload = current_app.config['UPLOAD_FOLDER']
        os.makedirs(pasta_upload, exist_ok=True)
        caminho_imagem = os.path.join(pasta_upload, nome_seguro)
        imagem.save(caminho_imagem)

        caminho_relativo = os.path.join('img', 'upload', nome_seguro).replace("\\", "/")

        try:
            conn = get_connection()
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
            return f"<h3 style='text-align:center;'>Erro ao salvar no banco: {erro_msg}</h3>"

    return "<h3 style='text-align:center;'>Erro: imagem não enviada.</h3>"