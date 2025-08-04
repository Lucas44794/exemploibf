from .home import home_bp
from .admin import admin_bp
from .painel import painel_bp
from .upload import upload_bp
from .excluir import excluir_bp
from .contato import contato_bp

def register_routes(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(painel_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(excluir_bp)
    app.register_blueprint(contato_bp)