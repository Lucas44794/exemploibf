from flask import Blueprint, render_template

clinica_bp = Blueprint('clinica', __name__)

@clinica_bp.route('/clinica')
def clinica():
    return render_template('clinica.html')
