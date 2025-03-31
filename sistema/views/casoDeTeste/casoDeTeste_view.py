from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user
from sistema import app, db, require_roles 
from sistema.models.caso_teste.caso_teste_model import CasoDeTesteModel
from sistema.models.projeto.projeto_model import ProjetoModel


@app.route('/listarCasoDeTeste')
@require_roles
def caso_listar():
    projetos = ProjetoModel.query.all()
  
    caso_id = request.args.get('projeto_id')  # Obtém o projeto_id passado pela URL
    
    if caso_id:
        # Filtra por projeto_id e somente casos ativos
        casosDeTestes = CasoDeTesteModel.query.filter_by(projeto_id=caso_id, ativo=1).all()
        
        # Busca o nome do projeto pelo projeto_id
        projeto_atual = ProjetoModel.query.get(caso_id)
    else:
        # Se nenhum projeto_id for passado, filtra apenas casos ativos
        casosDeTestes = CasoDeTesteModel.query.filter_by(ativo=1).all()
        projeto_atual = None  # Nenhum projeto específico selecionado

    return render_template('casoDeTeste/casoDeTeste_listar.html', casosDeTestes=casosDeTestes, projetos=projetos, projeto_atual=projeto_atual)


@app.route('/cadastrarCasoDeTeste', methods=['GET', 'POST'])
@require_roles
def caso_cadastrar():
    if current_user.is_authenticated:
        usuario_id = current_user.id  
        
        if request.method == 'POST': 
            campo_projeto = request.form.get('campoProjeto')
            campo_status = request.form.get('campoStatus')
            campo_titulo = request.form.get('campoTitulo')
            campo_objetivo = request.form.get('campoObjetivo')
            campo_passos = request.form.get('campoPassos')
            campo_resultadoEsperado = request.form.get('campoResultadoEsperado')
            campo_observacoes = request.form.get('campoObservacoes')
        
            caso_existente = CasoDeTesteModel.query.filter_by(titulo=campo_titulo).first()
            if caso_existente:
                flash("Caso de teste já cadastrado!", "danger")
                return redirect(url_for('caso_cadastrar'))
        
            casoDeTeste = CasoDeTesteModel(
                titulo = campo_titulo,
                status=campo_status,
                objetivo=campo_objetivo,
                passos=campo_passos,
                resultado_esperado=campo_resultadoEsperado,
                observacoes=campo_observacoes,
                usuario_id=usuario_id,
                projeto_id=campo_projeto
            )
            db.session.add(casoDeTeste)
            db.session.commit()
        
            flash("Caso de Teste cadastrado com sucesso!", "success")
            return redirect(url_for('caso_listar'))
    return render_template('casoDeTeste/casoDeTeste_listar.html')
        



@app.route("/casoDeTeste/editar/<int:id>", methods=['GET', 'POST'])
@require_roles
def caso_editar(id):
    projetos = ProjetoModel.query.all()
    
    if not current_user.is_authenticated:
        flash("Você precisa estar logado para acessar esta página.", "danger")
        return redirect(url_for('login'))  # Redireciona se não estiver autenticado

    usuario_id = current_user.id  
    casoDeTeste = CasoDeTesteModel.query.get(id)

    if not casoDeTeste:
        flash("Caso de Teste não encontrado!", "danger")
        return redirect(url_for('caso_listar'))  

    if request.method == 'POST': 
        campo_projeto = request.form.get('campoProjeto')
        campo_status = request.form.get('campoStatus')
        campo_titulo = request.form.get('campoTitulo')
        campo_objetivo = request.form.get('campoObjetivo')
        campo_passos = request.form.get('campoPassos')
        campo_resultadoEsperado = request.form.get('campoResultadoEsperado')
        campo_observacoes = request.form.get('campoObservacoes')

       
        caso_existente = CasoDeTesteModel.query.filter(
            CasoDeTesteModel.titulo == campo_titulo, CasoDeTesteModel.id != id
        ).first()

        if caso_existente:
            flash("Já existe um caso de teste com este título!", "danger")
            return redirect(url_for('caso_editar', id=id))
      
        casoDeTeste.titulo = campo_titulo
        casoDeTeste.status = campo_status
        casoDeTeste.objetivo = campo_objetivo
        casoDeTeste.passos = campo_passos
        casoDeTeste.resultado_esperado = campo_resultadoEsperado
        casoDeTeste.observacoes = campo_observacoes
        casoDeTeste.usuario_id = usuario_id
        casoDeTeste.projeto_id = campo_projeto

        db.session.commit()

        flash("Caso de teste atualizado com sucesso!", "success")
        return redirect(url_for('caso_listar', projeto_id=casoDeTeste.projeto_id)) 
    
    return render_template('casoDeTeste/casoDeTeste_editar.html', caso=casoDeTeste, projetos = projetos)


@app.route("/casoDeTeste/excluir/<int:id>", methods=['GET', 'POST'])
@require_roles
def caso_excluir(id):
    
    casoDeTeste = CasoDeTesteModel.query.get(id)

    if not casoDeTeste:
        flash("Caso de Teste não encontrado!", "danger")
        return redirect(url_for("caso_listar"))

    casoDeTeste.ativo = 0  # Marcar como inativo
    casoDeTeste.deletado = 1  # Marcar como deletado
    db.session.commit()

    flash("Caso de teste excluído com sucesso!", "success")

    # Agora, redirecione para a listagem de casos de teste ativos
    return redirect(url_for('caso_listar', projeto_id=casoDeTeste.projeto_id)) 


@app.route('/casoDeTeste/visualizar/<int:id>')
@require_roles
def caso_visualizar(id):
    casoDeTeste = CasoDeTesteModel.query.get(id)
    if not casoDeTeste:
        flash("Caso de Teste não encontrado!", "danger")
        return redirect(url_for("caso_listar"))
    return render_template('casoDeTeste/casoDeTeste_visualizar.html', caso=casoDeTeste)
