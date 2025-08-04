from flask import Blueprint, render_template
from db import get_connection
from psycopg2.extras import RealDictCursor

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM carousel ORDER BY id DESC")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        slides = [dict(zip(columns, row)) for row in rows]
        conn.close()
        return render_template('index.html', slides=slides)
    except Exception as e:
        erro_msg = str(e).encode('utf-8', errors='replace').decode('utf-8', errors='replace')
        return f"<h3 style='text-align:center;'>Erro ao carregar slides: {erro_msg}</h3>"