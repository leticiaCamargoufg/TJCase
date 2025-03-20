import os
from flask import render_template, request, redirect, url_for, flash
from sistema import app, db, require_roles  # Importa app corretamente
from sistema.models.autenticacao.role_model import RoleModel
from sistema.models.autenticacao.usuario_model import UsuarioModel
from sistema.models.upload_arquivo.upload_arquivo_model import UploadArquivoModel
from werkzeug.utils import secure_filename

from sistema.utils import allowed_file

@app.route('/usuarios')
@require_roles
def usuarios_listar():
    usuarios = UsuarioModel.query.all()
    return render_template('autenticacao/usuarios_listar.html', usuarios=usuarios)

@app.route('/usuario/cadastrar', methods=['GET', 'POST'])
@require_roles
def usuario_cadastrar():
    cargos = RoleModel.busca_roles_asc_cargo()

    if request.method == 'POST': 
        campo_nome = request.form.get('campoNome')
        campo_email = request.form.get('campoEmail')
        campo_senha = request.form.get('campoSenha')
        campo_confirmar_senha = request.form.get('campoConfirmarSenha')
        campo_cargo_id = request.form.get('campoCargo')

        if campo_senha != campo_confirmar_senha:
            flash("As senhas não coincidem!", "danger")
            return redirect(url_for('usuario_cadastrar'))

        usuario_existente = UsuarioModel.query.filter_by(email=campo_email).first()
        if usuario_existente:
            flash("E-mail já cadastrado!", "danger")
            return redirect(url_for('usuarios_cadastrar'))
        
        campo_foto = request.files['campoFotoPerfil']
        foto_id = None  

        if campo_foto and allowed_file(campo_foto.filename):
            nome_arquivo = secure_filename(f"{campo_email}_{campo_foto.filename}")
            caminho_arquivo = f"uploads/{nome_arquivo}"
            
            # Obtém UPLOAD_FOLDER do app configurado corretamente
            upload_folder = app.config.get("UPLOAD_FOLDER")

            if not upload_folder:
                raise RuntimeError("UPLOAD_FOLDER não está configurado corretamente!")

            campo_foto.save(os.path.join(upload_folder, nome_arquivo))

            arquivo = UploadArquivoModel(
                nome=nome_arquivo,
                caminho=caminho_arquivo,
                extensao=nome_arquivo.rsplit(".", 1)[1],
                tamanho=str(os.path.getsize(os.path.join(upload_folder, nome_arquivo)))
            )

            db.session.add(arquivo)
            db.session.commit()

            foto_id = arquivo.id
            
        user = UsuarioModel(
            nome=campo_nome,
            email=campo_email,
            senha_hash="",
            role_id=campo_cargo_id,
            ativo=True,
            foto_perfil_id=foto_id
        )
        user.set_password(campo_senha)
        db.session.add(user)
        db.session.commit()

        flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for('usuarios_listar'))

    return render_template('autenticacao/usuario_cadastrar.html', cargos=cargos)


@app.route("/usuario/editar/<int:id>", methods=['GET', 'POST'])
@require_roles
def usuario_editar(id):
    cargos = RoleModel.busca_roles_asc_cargo() 
    usuario = UsuarioModel.query.filter_by(id=id).first()
    
    if not usuario:
        flash("Usuário não encontrado!", "danger")
        return redirect(url_for('listar_usuarios'))  # Redireciona para a lista de usuários se não encontrar
    
    if request.method == 'POST':
        usuario.nome = request.form.get('campoNome')
        usuario.email = request.form.get('campoEmail')
        usuario.senha_hash = request.form.get('campoSenha')  
        confirmarSenha = request.form.get('campoConfirmarSenha')
        usuario.role_id = request.form.get('campoCargo')
        usuario.ativo = True
        
        if usuario.senha_hash != confirmarSenha:
            flash("As senhas não coincidem!", "danger")
            return redirect(url_for('usuario_cadastrar'))
        
        usuario.set_password(usuario.senha_hash)
        db.session.commit()  # Salva as alterações no banco
        flash("Usuário atualizado com sucesso!", "success")
        return redirect(url_for('usuarios_listar'))  # Redireciona após salvar

    return render_template("autenticacao/usuario_editar.html", usuario=usuario, cargos=cargos)


@app.route("/usuario/excluir/<int:id>", methods=['GET', 'POST'])
@require_roles
def usuario_excluir(id):
    usuario = UsuarioModel.query.filter_by(id=id).first()

    if not usuario:
        flash("Usuário não encontrado!", "danger")
        return redirect(url_for("usuarios_listar"))

    usuario.ativo = 0  # Define a coluna 'ativo' como 0 (desativado)
    db.session.commit()  # Salva a alteração no banco

    flash("Usuário desativado com sucesso!", "success")
    usuarios = UsuarioModel.query.all()
    return redirect(url_for('usuarios_listar', usuarios=usuarios))