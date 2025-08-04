from flask import Blueprint, render_template
from db import get_connection
from psycopg2.extras import RealDictCursor

painel_bp = Blueprint('painel', __name__)

@painel_bp.route('/painel')
def painel():
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM carousel ORDER BY id DESC")
        slides = cursor.fetchall()
        conn.close()
        return render_template('painel.html', slides=slides)
    except Exception as e:
        erro_msg = str(e)
        return f"<h3 style='text-align:center;'>Erro ao conectar com o banco: {erro_msg}</h3>"