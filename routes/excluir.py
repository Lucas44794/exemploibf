import os
from flask import Blueprint, redirect
from db import get_connection

excluir_bp = Blueprint('excluir', __name__)

@excluir_bp.route('/excluir/<int:slide_id>', methods=['POST'])
def excluir_slide(slide_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT imagem FROM carousel WHERE id = %s", (slide_id,))
        resultado = cursor.fetchone()

        if resultado and resultado[0]:
            caminho_imagem = os.path.join('static', resultado[0])
            if os.path.exists(caminho_imagem):
                os.remove(caminho_imagem)

        cursor.execute("DELETE FROM carousel WHERE id = %s", (slide_id,))
        conn.commit()
        conn.close()
        return redirect('/painel')
    except Exception as e:
        erro_msg = str(e)
        return f"<h3 style='text-align:center;'>Erro ao excluir: {erro_msg}</h3>"