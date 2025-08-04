from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_mail import Message
from datetime import datetime

contato_bp = Blueprint('contato', __name__)

@contato_bp.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        try:
            nome = request.form.get('nomesobrenome')
            email = request.form.get('email')
            telefone = request.form.get('telefone')
            mensagem = request.form.get('mensagem')
            curso = request.form.get('cursosescolhidos')
            horario = request.form.get('horario')
            modalidade = request.form.get('modalidade')
            ip = request.remote_addr

            msg = Message(
                subject='Novo Formulário de Contato',
                recipients=['lucasr.prodata@gmail.com']
            )
            msg.body = f"""
            Nome: {nome}
            E-mail: {email}
            Telefone: {telefone}
            Mensagem: {mensagem}
            Curso Escolhido: {curso}
            Horário Preferido: {horario}
            Modalidade do Curso: {modalidade}
            IP: {ip}
            Enviado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
            """
            current_app.mail.send(msg)
            return redirect(url_for('contato.contato', success=True))
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
            return render_template('contato.html', erro_envio=True)

    return render_template('contato.html')