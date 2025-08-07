from flask import Blueprint, render_template
from db import get_connection
from psycopg2.extras import RealDictCursor

escola_bp = Blueprint('escola', __name__)

@escola_bp.route('/escola')
def escola():
    return render_template('escola.html')