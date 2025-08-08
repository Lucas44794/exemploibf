from flask import Blueprint, render_template
from db import get_connection
from psycopg2.extras import RealDictCursor

seminario_bp = Blueprint('seminario', __name__)

@seminario_bp.route('/seminario')
def seminario():
    return render_template('seminario.html')