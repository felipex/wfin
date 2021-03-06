from app import db
from datetime import date

class Responsavel(db.Model):
    #__table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(124), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    rg = db.Column(db.String(20), unique=True, nullable=False)
    telefone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    endereco = db.Column(db.String(120), nullable=True)
    bairro = db.Column(db.String(50), nullable=True)
    cidade = db.Column(db.String(50), nullable=True)
    uf = db.Column(db.String(2), nullable=True)
    cep = db.Column(db.String(10), nullable=True)

    def __init__(self, nome, cpf, rg):
        self.nome = nome
        self.cpf = cpf
        self.rg = rg
        
        
    def __repr__(self):
        return u'<Responsavel %r>' % self.nome
   
    
class Contrato(db.Model):
    FORMAS = (
        ('E', 'Espécie'),
        ('C', 'Cheque'),
        ('B', 'Boleto'),
        ('T', 'Cartão'),
    )

    id = db.Column(db.Integer, primary_key=True)
    aluno = db.Column(db.String(128))
    responsavel_id = db.Column(db.Integer, db.ForeignKey("responsavel.id"))
    parentesco = db.Column(db.String(20), nullable=True)
    serie = db.Column(db.String(20), nullable=True)
    ano = db.Column(db.Integer, nullable=False)
    vencimento = db.Column(db.Integer, nullable=False, default=5)
    data = db.Column(db.Date, nullable=True)
    forma_de_pgto = db.Column(db.String(1), nullable=True)
    anotacoes = db.Column(db.Text, nullable=True, default='')
    valor = db.Column(db.Float, nullable=False, default=0.0)
    

    def __init__(self):
        self.aluno = ''
        self.responsavel_id = 0
        self.parentesco = ''
        self.serie = ''
        self.ano = ''
        self.vencimento = 5
        self.carnet_entregue = False

    def numero(self):
        if self.id is None: # No caso da criação de um novo contrato.
            return ''
        else:
            return "%s%04d" % (self.ano, self.id) 
        
        
    def responsavel(self):
        return Responsavel.query.get(self.responsavel_id)
        
        
    def prestacoes(self):
        return db.session.query(Prestacao).filter(Prestacao.contrato_id==self.id)
        
        
    def create_prestacoes(self, valor):
        for mes in range(1,13):
            p = Prestacao()
            p.contrato_id = self.id
            p.mes = mes
            p.valor = valor;
            p.vencimento = date(self.ano, mes, self.vencimento)
            if p.vencimento < date.today():
                p.status = 'N'
            else:
                p.status = 'A'
            db.session.add(p)
            
        db.session.commit()

    @staticmethod
    def filter(text):
        l1 = db.session.query(Contrato).filter(Contrato.aluno.like("%"+text+"%"))
        return l1

        
    @staticmethod
    def abertos():
        pass


    @staticmethod
    def inadimplentes():
        cc = Contrato.query.all()
        inad = []
        for c in cc:
            em_atraso = False
            for p in c.prestacoes():
                em_atraso = em_atraso or p.em_atraso()
                
            if em_atraso:
                inad.append(c)

        return inad


class Prestacao(db.Model):
    FORMAS = (
        ('E', 'Espécie'),
        ('C', 'Cheque'),
        ('B', 'Boleto'),
        ('T', 'Cartão'),
    )
    
    STATUS = (
        ('A', 'Aberto'),
        ('P', 'Pago'),
        ('D', 'Desistente'),
        ('N', 'Não Estudou'),
    )
    id = db.Column(db.Integer, primary_key=True)
    
    contrato_id = db.Column(db.Integer, db.ForeignKey("contrato.id"))

    mes = db.Column(db.Integer)
    vencimento = db.Column(db.Date, nullable=False)
    valor = db.Column(db.Float, nullable=False, default=0.0)

    data_pgto = db.Column(db.Date, nullable=True)
    valor_pago = db.Column(db.Float, nullable=True, default=0.0)
    status = db.Column(db.String(1), nullable=False, default='A')
    
    forma_de_pgto = db.Column(db.String(1), nullable=True)
    cheque_numero = db.Column(db.String(10), nullable=True)
    cheque_data = db.Column(db.Date, nullable=True)
    
    
    def contrato(self):
        return Contrato.query.get(self.contrato_id)
        
    @staticmethod    
    def pagamentos_com_cheque(di, df):
        return Prestacao.query.filter_by(forma_de_pgto='C').\
        filter(Prestacao.cheque_data>=di, Prestacao.cheque_data<=df).order_by(Prestacao.cheque_data).all()
        
    
    @staticmethod    
    def faturamento(ano):
        from jinja2 import Environment
        env = Environment()
        print(dir(env))
        
        previsao = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
        recebido = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
        inadimplente = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
        cc = Contrato.query.filter_by(ano=ano)
        for c in cc:
            for p in c.prestacoes():
                if (p.status == 'P') or (p.status == 'A'):
                    previsao[p.vencimento.month-1] = previsao[p.vencimento.month-1] + p.valor 
                    
                if p.data_pgto:
                    recebido[p.data_pgto.month-1] = recebido[p.data_pgto.month-1] + p.valor_pago
                    
                if p.em_atraso():
                    inadimplente[p.vencimento.month-1] = inadimplente[p.vencimento.month-1] + p.valor
                
                    
        return previsao, recebido, inadimplente        
    
    
    def messtr(self):
        return ('Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro')[self.mes-1]
        
    
    def statusstr(self):
        return dict(self.STATUS)[self.status]
        
    def forma_de_pgto_str(self):
        try:
            return dict(self.FORMAS)[self.forma_de_pgto]
        except:
            return ''
        
    def valorstr(self):
        return "{:,.2f}".format(self.valor).replace('.', 'o').replace(',', '.').replace('o', ',')
        
    
    def cheque_data_str(self):
        if (self.cheque_data):
            return self.cheque_data.strftime('%d-%m-%Y')
    
        
    def em_atraso(self):
        if (self.status == 'A'):
            if (self.vencimento < date.today()):
                return True
        return False
        
