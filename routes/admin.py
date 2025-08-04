from flask import Blueprint, render_template, request, redirect
from db import get_connection

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['password']
        try:
            conn = get_connection()
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
            return f"<h3 style='text-align:center;'>Erro ao salvar no banco: {erro_msg}</h3>"
    return render_template('login.html')