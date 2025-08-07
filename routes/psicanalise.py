from flask import Blueprint, render_template

psicanalise_bp = Blueprint('psicanalise', __name__)

@psicanalise_bp.route('/psicanalise')
def psicanalise():
    return render_template('psicanalise.html')


