import datetime
from datetime import date
from flask import render_template, request, redirect, url_for, flash, session, abort, send_from_directory
from app import app, db
from app.models import Responsavel, Contrato, Prestacao
from app.forms import RespForm, ContratoForm, PrestacaoForm, PagamentoForm
from app.filters import formatfloat

def form_to_resp(form, resp):
    resp.nome = form["nome"] 
    resp.cpf = form["cpf"] 
    resp.rg = form["rg"]
    resp.telefone = form["telefone"]
    resp.email = form["email"]
    resp.endereco = form["endereco"]
    resp.bairro = form["bairro"]
    resp.cidade = form["cidade"]
    resp.uf = form["uf"]
    resp.cep = form["cep"]

def verifica_login():
    if session['logged_in']:
        return True
    else:
        abort(401)

@app.errorhandler(401)
def nao_autorizado(e):
    return redirect(url_for("do_login"))
    
    
@app.route('/login', methods=['GET', 'POST'])
def do_login():
 
    if request.method == 'POST':
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])
     
        if (POST_USERNAME == 'admin') and (POST_PASSWORD == 'wfin2018'):
            session['logged_in'] = True
            session['username'] = POST_USERNAME 
        else:
            flash('Usuário ou senha incorretos!')
        return index()
    else:
        return render_template("login-form.html")
        
 
def authenticate(func):
    def wrapper(*args, **kwargs):
        try:
            print(session['logged_in'])
            if session['logged_in']: 
                return func(*args, **kwargs)
            else:
                return redirect(url_for("do_login"))
        except:
            return redirect(url_for("do_login"))
                    
    return wrapper

 
@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['username'] = ''
    return redirect(url_for("do_login"))

        
@app.route("/", methods=['GET'])
#@authenticate
def index():
    verifica_login()
    return render_template("index.html")


@app.route("/consultas", methods=['GET'])
def consultas():
    verifica_login()
    return render_template("consultas.html")


@app.route("/consulta/geral", methods=['GET'])
def consulta_geral():
    verifica_login()
    busca = request.args.get("busca", default="")
    lista = Contrato.filter(busca) 
    return render_template("consulta-geral.html", lista=lista)


@app.route("/consulta/inadimplentes", methods=['GET'])
def consulta_inadimplentes():
    verifica_login()
    lista = Contrato.inadimplentes() 
    totais = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    for l in lista:
        for p in l.prestacoes():
            if p.em_atraso():
                totais[p.mes-1] += p.valor 
    return render_template("consulta-inadimplentes.html", lista=lista, totais=totais, formatfloat=formatfloat)
    
@app.route("/consulta/faturamento", methods=['GET'])
def consulta_faturamento():
    verifica_login()
    previsao, recebido, em_atraso = Prestacao.faturamento(2018) 
    total = {
        'previsao': sum(previsao),
        'recebido': sum(recebido),
        'em_atraso': sum(em_atraso)
    }
    return render_template("consulta-faturamento.html", formatfloat=formatfloat, previsao=previsao, recebido=recebido, em_atraso=em_atraso, total=total, data=date.today())


@app.route("/consulta/chequepre", methods=['GET'])
def chequepre():
    verifica_login()
    today = date.today()
    mesi = today.replace(day=1)
    mesf = mesi.replace(month=mesi.month+1) - datetime.timedelta(days=1)
    return render_template("consulta-chequepre.html", datai=mesi, dataf=mesf)


#########################################
##  Responsável
#########################################

@app.route("/responsavel/list", methods=['GET'])
def responsavel_list():
    verifica_login()
    busca = request.args.get("busca", default="")
    rr = db.session.query(Responsavel).filter(Responsavel.nome.like("%"+busca+"%"))
    return render_template("responsavel-list.html", rr=rr)
    

@app.route("/responsavel/edit/<int:rid>", methods=['GET', 'POST'])
def responsavel_edit(rid=0):
    verifica_login()
    r = Responsavel.query.get(rid)
    if request.method == 'POST':                 
        form_to_resp(request.form, r)
        db.session.add(r)
        db.session.commit()
        flash("Operação realizada com sucesso")

        return redirect(url_for("responsavel_list"))
        #rr = Responsavel.query.all()    
        #return render_template("responsavel-list.html", rr=rr)
    else:
        form = RespForm()   
        return render_template("responsavel-form.html", form=form, r=r)


@app.route("/responsavel/add", methods=['GET', 'POST'])
def responsavel_add():
    verifica_login()
    r = Responsavel('','','');
    if request.method == 'POST':
        form_to_resp(request.form, r)
        print("telefone ", r.telefone)
        db.session.add(r)
        db.session.commit()
        flash("Operação realizada com sucesso")
        return redirect(url_for("responsavel_list"))

             
    form = RespForm()   
    return render_template("responsavel-form.html", form=form, r=r)


#########################################
##  Contrato
#########################################
@app.route("/contrato/list", methods=['GET'])
def contrato_list():
    verifica_login()
    busca = request.args.get("busca", default="")
    lista = Contrato.filter(busca) #db.session.query(Contrato).filter(Contrato.aluno.like("%"+busca+"%"))
    return render_template("contrato-list.html", lista=lista)
    
def strtodate(s):
    ano, mes, dia = s.split('/')
    return date(int(dia), int(mes), int(ano))

    
def datetostr(date):
    return date.strftime('%d/%m/%Y')


def str_to_float(svalor):
    return float(svalor.replace('.','').replace(',', '.'))


def form_to_contrato(form, obj):
    obj.aluno = form['aluno']
    obj.responsavel_id = int(form['responsavel_id'])
    obj.parentesco = form['parentesco']
    obj.serie = form['serie']
    obj.ano = form['ano']
    obj.vencimento = form['vencimento']
    obj.data = strtodate(form['data'])
    obj.forma_de_pgto = form['forma_de_pgto']
    obj.valor = str_to_float(form['valor'])
    obj.anotacoes = form['anotacoes']
    
    if form.get('carnet_entregue', False) == 'on':
        obj.carnet_entregue = True 
    else:
        obj.carnet_entregue = False 
    
        

def display_data(data):
    if (data):
        return datetostr(data)
    else:
        return datetostr(date.today())


@app.route("/contrato/edit/<int:cid>", methods=['GET', 'POST'])
def contrato_edit(cid=0):
    verifica_login()
    obj = Contrato.query.get(cid)
    resps = Responsavel.query.order_by('nome')
    
    if request.method == 'POST':       
        form_to_contrato(request.form, obj)

        db.session.add(obj)
        db.session.commit()
        return redirect(url_for("contrato_list"))
    else:
        form = ContratoForm()
        data = display_data(obj.data)      
        
        return render_template("contrato-form.html", form=form, obj=obj, resps=resps, data=data)


@app.route("/contrato/add", methods=['GET', 'POST'])
def contrato_add():
    verifica_login()
    obj = Contrato()
    obj.data = date.today()
    resps = Responsavel.query.order_by('nome')

    if request.method == 'POST':
        form_to_contrato(request.form, obj)
        
        db.session.add(obj)
        db.session.commit()
        obj.create_prestacoes(obj.valor)
        return redirect(url_for("contrato_list"))
    else:
        form = ContratoForm()
        data = display_data(obj.data)
        return render_template("contrato-form.html", form=form, obj=obj, resps=resps)


#########################################
##  Prestações
#########################################
@app.route("/prestacao/list/<int:cid>", methods=['GET'])
def prestacao_list(cid=0):
    verifica_login()
    obj = Contrato.query.get(cid)
    prests = obj.prestacoes().all()
    
    return render_template("prestacao-list.html", obj=obj, prests=prests)


def form_to_prestacao(form, obj):
    obj.vencimento = form['vencimento']
    obj.valor = form['valor']
    obj.status = form['status']
    if (form['data_pgto'] != ''):
        obj.data_pgto = form['data_pgto']
    obj.valor_pago = form['valor_pago']
    obj.forma_de_pgto = form['forma_pgto']
    if obj.forma_de_pgto == 'C':
        obj.cheque_numero = form['cheque_numero'] 
        obj.cheque_data = form['cheque_data']
    

@app.route("/prestacao/edit/<int:pid>", methods=['GET', 'POST'])
def prestacao_edit(pid=0):
    verifica_login()
    obj = Prestacao.query.get(pid)
    
    if request.method == 'POST':
        form_to_prestacao(request.form, obj)
        
        #db.session.add(obj)
        db.session.commit()
        return redirect("/prestacao/list/%d" % obj.contrato_id)
    else:
        form = PrestacaoForm()
    
        form.mes.value = obj.mes
        form.vencimento.value = obj.vencimento
        form.valor.value = obj.valor

        form.status = obj.status
        form.data_pgto.value = obj.data_pgto
        form.valor_pago.value = obj.valor_pago
        
        form.forma_de_pgto.value = obj.forma_de_pgto 
        form.cheque_numero.value = obj.cheque_numero
        form.cheque_data.value = obj.cheque_data

        return render_template("prestacao-form.html", obj=obj, form=form)


@app.route("/pagamentos/list/<int:cid>", methods=['GET'])
def pagamentos_list(cid=0):
    verifica_login()
    obj = Contrato.query.get(cid)
    prests = obj.prestacoes().all()
    
    return render_template("pagamentos-list.html", obj=obj, prests=prests)
    

@app.route("/prestacao/naoestudou/<int:pid>", methods=['GET'])
def prestacao_naoestudou(pid=0):
    verifica_login()
    obj = Prestacao.query.get(pid)
    obj.status = "N"
    db.session.commit()
    return redirect("/prestacao/list/%d" % obj.contrato_id)


@app.route("/prestacao/reabre/<int:pid>", methods=['GET'])
def prestacao_reabre(pid=0):
    verifica_login()
    obj = Prestacao.query.get(pid)
    obj.status = "A"
    db.session.commit()
    return redirect("/prestacao/list/%d" % obj.contrato_id)


@app.route("/prestacao/desistiu/<int:pid>", methods=['GET'])
def prestacao_desistiu(pid=0):
    verifica_login()
    obj = Prestacao.query.get(pid)
    obj.status = "D"
    db.session.commit()
    flash("Operação realizada com sucesso")
    return redirect("/prestacao/list/%d" % obj.contrato_id)


@app.route("/prestacao/pagamento/<int:pid>", methods=['GET', 'POST'])
def pagamento_prestacao(pid=0):
    verifica_login()
    obj = Prestacao.query.get(pid)
    
    if request.method == 'POST':
        obj.status = "P"
        obj.data_pgto = strtodate(request.form['data_pgto'])
        obj.valor_pago = request.form['valor_pago']
        obj.forma_de_pgto = request.form['forma_de_pgto']
        if obj.forma_de_pgto == 'C':
            obj.cheque_numero = request.form['cheque_numero'] 
            obj.cheque_data = strtodate(request.form['cheque_data'])
        else:
            obj.cheque_numero = '' 
            obj.cheque_data = None
        
        
        db.session.commit()
        return redirect("/pagamentos/list/%d" % obj.contrato_id)
    else:
        form = PagamentoForm()
    
        form.mes.value = obj.mes
        form.vencimento.value = obj.vencimento
        form.valor.value = obj.valor

        form.status = 'P'
        form.data_pgto.value = datetostr(date.today())
        form.valor_pago.value = obj.valor
        
        form.forma_de_pgto.value = 'E'
        form.cheque_numero.value = ''
        form.cheque_data.value = ''

        data_de_pgto = datetostr(date.today())
            
        return render_template("pagamento-form.html", obj=obj, form=form, data_de_pgto=data_de_pgto)



@app.route("/impressao/carnets/<int:cid>", methods=['GET'])
def impressao_carnets(cid=0):
    #https://codepen.io/rafaelcastrocouto/pen/LFAes
    #https://pt.stackoverflow.com/questions/149014/como-imprimir-p%C3%A1ginas-em-a4-utilizando-css
    #http://jsfiddle.net/2wk6Q/1/
    verifica_login()
    obj = Contrato.query.get(cid)
    prests = obj.prestacoes().all()
    
    return render_template("carnets.html", obj=obj, prests=prests)


@app.route("/impressao/contrato/<int:cid>", methods=['GET'])
def impressao_contrato(cid=0):
    verifica_login()
    obj = Contrato.query.get(cid)
    
    return render_template("impressao-contrato.html", obj=obj)


@app.route("/configuracao", methods=['GET'])
def configuracao():
    verifica_login()
    return render_template("configuracao.html")


import shutil 
from datetime import datetime
@app.route("/ferramenta/backup")
def backup():
    verifica_login()
    import os
    bk_name = 'app/database_%Y%m%d%H%M%S.db.bk'
    shutil.copy('app/database.db', datetime.today().strftime(bk_name))
    flash("Operação realizada com sucesso.")
    #send_from_directory('app', 'database.db', as_attachment=True)
    return render_template("mensagem.html")


@app.route("/init")
def init():
    verifica_login()
    db.create_all();
    return "<h1>Pronto</h1>"


def init2():
    verifica_login()
    db.create_all();

    r = Responsavel('Felipe Cavalcante', '111.222.333-44', '12345')
    r.telefone = '99999-9999'
    r.email = 'felipe@ufca'
    r.endereco = 'Rua Monsenhor Aze'
    r.bairro = 'betolandia'
    r.cidade = 'Juazeiro'
    r.uf = 'CE'
    r.cep = '63.031-200'
    db.session.add(r)
    
    r = Responsavel.query.first()
    c = Contrato()
    c.aluno = 'Pedro'
    c.responsavel_id = r.id
    c.parentesco = 'pai'
    c.serie = 'I5'
    c.ano = 2018
    c.vencimento = 5
    db.session.add(c)
    db.session.commit()
    c.create_prestacoes(100.00)

    r = Responsavel('Luiz Gonzaga', '222.222.333-44', '123456')
    r.telefone = '99999-9992'
    r.email = 'luiz@ufca'
    r.endereco = 'Av Monsenhor Aze'
    r.bairro = 'betolandia'
    r.cidade = 'Juazeiro'
    r.uf = 'CE'
    r.cep = '63.031-201'
    db.session.add(r)
    db.session.commit()
    
    r = Responsavel.query.first()
    c = Contrato()
    c.aluno = 'Gonzaguinha'
    c.responsavel_id = r.id
    c.parentesco = 'pai'
    c.serie = 'I4'
    c.ano = 2018
    c.vencimento = 10
    db.session.add(c)
    db.session.commit()
    c.create_prestacoes(100.00)

    return "<h1>Pronto</h1>"


#        <label>{{ form.responsavel.label }}</label> {{ form.responsavel(value=obj.responsavel_id, #class="form-control") }}

