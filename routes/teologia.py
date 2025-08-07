from flask import Blueprint, render_template

teologia_bp = Blueprint('teologia', __name__)

@teologia_bp.route('/teologia')
def teologia():
    return render_template('teologia.html')