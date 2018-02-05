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
   


class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128), unique=True, nullable=False)
    parentesco = db.Column(db.String(20), nullable=True)
    serie = db.Column(db.String(20), nullable=True)
    
    responsavel_id = db.Column(db.Integer, db.ForeignKey("responsavel.id"))
    
    #responsavel = db.relationship("Responsavel", foreign_key=responsavel_id)
    
    def __repr__(self):
        return u'<Aluno %r>' % self.nome
    
    
class Contrato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno = db.Column(db.String(128))
    responsavel_id = db.Column(db.Integer, db.ForeignKey("responsavel.id"))
    parentesco = db.Column(db.String(20), nullable=True)
    serie = db.Column(db.String(20), nullable=True)
    ano = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    vencimento = db.Column(db.Integer, nullable=False, default=5)
    carnet_entregue = db.Column(db.Boolean, nullable=False, default=False)
    anotacoes = db.Column(db.TextField, nullable=True, defaul='')
    valor = db.Column(db.Float, nullable=False, default=0.0)
    
"""    

    valor01 = db.Column(db.Float, nullable=False, default=0.0)
    valor02 = db.Column(db.Float, nullable=False, default=0.0)
    valor03 = db.Column(db.Float, nullable=False, default=0.0)
    valor04 = db.Column(db.Float, nullable=False, default=0.0)
    valor05 = db.Column(db.Float, nullable=False, default=0.0)
    valor06 = db.Column(db.Float, nullable=False, default=0.0)
    valor07 = db.Column(db.Float, nullable=False, default=0.0)
    valor08 = db.Column(db.Float, nullable=False, default=0.0)
    valor09 = db.Column(db.Float, nullable=False, default=0.0)
    valor10 = db.Column(db.Float, nullable=False, default=0.0)
    valor11 = db.Column(db.Float, nullable=False, default=0.0)
    valor12 = db.Column(db.Float, nullable=False, default=0.0)
    
    # 'A' - Aberto; 'P' - Pago; 'D'- Desistente; 'N' - Não Estudou
    mes01 = db.Column(db.String(1), nullable=False, default='A')  
    mes02 = db.Column(db.String(1), nullable=False, default='A')    
    mes03 = db.Column(db.String(1), nullable=False, default='A')    
    mes04 = db.Column(db.String(1), nullable=False, default='A')    
    mes05 = db.Column(db.String(1), nullable=False, default='A')    
    mes06 = db.Column(db.String(1), nullable=False, default='A')    
    mes07 = db.Column(db.String(1), nullable=False, default='A')    
    mes08 = db.Column(db.String(1), nullable=False, default='A')    
    mes09 = db.Column(db.String(1), nullable=False, default='A')    
    mes10 = db.Column(db.String(1), nullable=False, default='A')    
    mes11 = db.Column(db.String(1), nullable=False, default='A')    
    mes12 = db.Column(db.String(1), nullable=False, default='A')    

    pago01 = db.Column(db.Float, nullable=False, default=0.0)
    pago02 = db.Column(db.Float, nullable=False, default=0.0)
    pago03 = db.Column(db.Float, nullable=False, default=0.0)
    pago04 = db.Column(db.Float, nullable=False, default=0.0)
    pago05 = db.Column(db.Float, nullable=False, default=0.0)
    pago06 = db.Column(db.Float, nullable=False, default=0.0)
    pago07 = db.Column(db.Float, nullable=False, default=0.0)
    pago08 = db.Column(db.Float, nullable=False, default=0.0)
    pago09 = db.Column(db.Float, nullable=False, default=0.0)
    pago10 = db.Column(db.Float, nullable=False, default=0.0)
    pago11 = db.Column(db.Float, nullable=False, default=0.0)
    pago12 = db.Column(db.Float, nullable=False, default=0.0)
"""
    def __init__(self):
        self.aluno = ''
        self.responsavel_id = 0
        self.parentesco = ''
        self.serie = ''
        self.ano = ''
        self.vencimento = 5
        self.carnet_entregue = False
        
    def create_prestacoes(valor):
        for mes in range(1,13):
            p = Prestacao()
            p.valor = valor;
            p.vencimento = date(self.ano, mes, self.vencimento)
            p.status = 'A'
            db.session.add(p)
            
        db.session.commit()


"""
        self.valor01 = 0.00
        self.valor02 = 0.00
        self.valor03 = 0.00
        self.valor04 = 0.00
        self.valor05 = 0.00
        self.valor06 = 0.00
        self.valor07 = 0.00
        self.valor08 = 0.00
        self.valor09 = 0.00
        self.valor10 = 0.00
        self.valor11 = 0.00
        self.valor12 = 0.00
        
        # 'A' - Aberto; 'P' - Pago; 'D'- Desistente; 'N' - Não Estudou
        #self.mes01 = 'A'  
        self.mes02 = 'A'    
        self.mes03 = 'A'    
        self.mes04 = 'A'    
        self.mes05 = 'A'    
        self.mes06 = 'A'    
        self.mes07 = 'A'    
        self.mes08 = 'A'    
        self.mes09 = 'A'    
        self.mes10 = 'A'    
        self.mes11 = 'A'    
        self.mes12 = 'A'    

        self.pago01 = 0.00
        self.pago02 = 0.00
        self.pago03 = 0.00
        self.pago04 = 0.00
        self.pago05 = 0.00
        self.pago06 = 0.00
        self.pago07 = 0.00
        self.pago08 = 0.00
        self.pago09 = 0.00
        self.pago10 = 0.00
        self.pago11 = 0.00
        self.pago12 = 0.00
"""

class Prestacao(db.Model):
    FORMAS = (
        ('E', 'Espécie'),
        ('C', 'Cheque'),
    )
    
    STATUS = (
        ('A', 'Aberto'),
        ('P', 'Pago'),
        ('D', 'Desistente'),
        ('N', 'Não Estudou'),
    )
    
    contrato_id = db.Column(db.Integer, db.ForeignKey("contrato.id"))

    vencimento = db.Column(db.DateTime, nullable=False)
    valor = db.Column(db.Float, nullable=False, default=0.0)

    data_pgto = db.Column(db.DateTime, nullable=True)
    valor_pago = db.Column(db.Float, nullable=True, default=0.0)
    status = db.Column(db.String(1), nullable=False, default='A')
    
    forma_de_pgto = db.Column(db.String(1), nullable=True)
    cheque_numero = db.Column(db.String(10), nullable=True)
    cheque_data = db.Column(db.DateTime, nullable=True)
    

