from .home import home_bp
from .admin import admin_bp
from .painel import painel_bp
from .upload import upload_bp
from .excluir import excluir_bp
from .contato import contato_bp
from .escola import escola_bp
from .prospere import prospere_bp
from .teologia import teologia_bp
from .psicanalise import psicanalise_bp
from .clinica import clinica_bp

def register_routes(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(painel_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(excluir_bp)
    app.register_blueprint(contato_bp)
    app.register_blueprint(escola_bp)
    app.register_blueprint(prospere_bp)
    app.register_blueprint(teologia_bp)
    app.register_blueprint(psicanalise_bp)
    app.register_blueprint(clinica_bp)