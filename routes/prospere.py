from flask import Blueprint, render_template
from db import get_connection
from psycopg2.extras import RealDictCursor

prospere_bp = Blueprint('prospere', __name__)

@prospere_bp.route('/prospere')
def prospere():
    return render_template('prospere.html')